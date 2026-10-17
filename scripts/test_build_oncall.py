#!/usr/bin/env python3
"""Tests for scripts/build_oncall.py (#36, ADR-0037): the rotation evaluator (waking hours, overnight shifts, rotation
turns, overrides), which issues count as pager records (author, label, pull requests, broken JSON), the page rows and
weeks, the contract check (a key outside the contract, a Discord-like ID or a URL in free text, html that differs from
the data), and the escaping of the html. Stdlib only; no network.

    python3 scripts/test_build_oncall.py

Exits 1 when a case fails.
"""
import copy, datetime, json, sys, unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_oncall as bo  # noqa: E402

UTC = datetime.timezone.utc
NOW = datetime.datetime(2026, 10, 17, 12, 0, tzinfo=UTC)  # Saturday 14:00 in Berlin
ROT = {
    'timezone': 'Europe/Berlin',
    'people': {'stefan': {'name': 'Stefan Coetzee', 'kind': 'human'}, 'ana': {'name': 'Ana', 'kind': 'human'},
               'responder': {'name': 'Responder agent', 'kind': 'agent'}},
    'schedules': {
        'primary': {'description': 'The operator, in waking hours.',
                    'layers': [{'name': 'Waking hours', 'members': ['stefan'], 'start': '2026-10-19T08:00', 'turn': '7d',
                                'restrictions': [{'days': bo.DAYS, 'from': '08:00', 'to': '22:00'}]}]},
        'responder': {'description': 'Read-only.', 'layers': [{'name': 'Always', 'members': ['responder']}]},
    },
    'escalation_policy': {'name': 'House default', 'rules': [{'after': '0m', 'schedule': 'primary'},
                                                            {'after': '15m', 'schedule': 'responder'}],
                          'renotify_after': '5m', 'renotify_limit': 3},
    'overrides': [],
}


def record(**kw):
    v = {'alert': 'OllamaDown', 'severity': 'page', 'prometheus': 'agent-observability', 'fired': '2026-10-17T10:00:00Z',
         'acknowledged': '2026-10-17T10:03:00Z', 'acknowledged_by': 'Stefan Coetzee', 'resolved': '2026-10-17T10:20:00Z',
         'resolved_by': 'Alertmanager', 'responder_ran': False, 'time_to_acknowledge_s': 180, 'time_to_resolve_s': 1200}
    v.update(kw)
    return v


def issue(views, login='uncovertechtalent', labels=('kind:finding', 'area:ai'), pr=False, body=None):
    i = {'user': {'login': login}, 'labels': [{'name': n} for n in labels],
         'body': body if body is not None else f'text\n<!-- pager-record {json.dumps(views)} -->\n'}
    if pr:
        i['pull_request'] = {}
    return i


class RotationTest(unittest.TestCase):
    def test_waking_hours_overnight_turns_and_overrides(self):
        self.assertEqual(bo.who(ROT, 'primary', NOW), 'stefan')
        self.assertIsNone(bo.who(ROT, 'primary', datetime.datetime(2026, 10, 17, 21, 0, tzinfo=UTC)))
        night = {'days': ['fri'], 'from': '22:00', 'to': '06:00'}
        self.assertTrue(bo.allows(night, datetime.datetime(2026, 10, 17, 5, 0)))   # Saturday 05:00 belongs to Friday
        self.assertFalse(bo.allows(night, datetime.datetime(2026, 10, 17, 23, 0)))
        rot = copy.deepcopy(ROT)
        rot['schedules']['primary']['layers'] = [{'name': 'base', 'members': ['stefan', 'ana'], 'start': '2026-10-12T08:00', 'turn': '7d'}]
        self.assertEqual(bo.who(rot, 'primary', datetime.datetime(2026, 10, 21, 12, 0, tzinfo=UTC)), 'ana')
        rot['overrides'] = [{'person': 'stefan', 'start': '2026-10-21T13:00', 'end': '2026-10-21T15:00'}]
        self.assertEqual(bo.who(rot, 'primary', datetime.datetime(2026, 10, 21, 12, 0, tzinfo=UTC)), 'stefan')

    def test_from_rotation_names_people_and_hours(self):
        d = bo.from_rotation(ROT, NOW)
        self.assertEqual([(o['schedule'], o['person'], o['kind']) for o in d['on_call']],
                         [('primary', 'Stefan Coetzee', 'human'), ('responder', 'Responder agent', 'agent')])
        self.assertEqual(d['layers'][0]['hours'], 'every day 08:00 to 22:00')
        self.assertEqual(d['policy']['steps'], [{'after_min': 0, 'schedule': 'primary'}, {'after_min': 15, 'schedule': 'responder'}])


class RecordsTest(unittest.TestCase):
    def test_only_the_machine_accounts_labelled_issues_count(self):
        self.assertEqual(len(bo.records_from_issue(issue([record()]))), 1)
        self.assertEqual(bo.records_from_issue(issue([record()], login='stranger')), [])
        self.assertEqual(bo.records_from_issue(issue([record()], labels=('area:ai',))), [])
        self.assertEqual(bo.records_from_issue(issue([record()], pr=True)), [])
        self.assertEqual(bo.records_from_issue(issue([], body='<!-- pager-record [nope -->')), [])
        self.assertEqual(bo.records_from_issue(issue([], body='no record')), [])

    def test_rows_drop_bad_entries_and_flag_out_of_hours(self):
        views = [record(), record(fired='2026-10-16T21:30:00Z'), record(alert='bad name!'), record(fired='yesterday'),
                 record(fired='2026-07-01T10:00:00Z'), record(acknowledged_by='Ste​fan <b>', time_to_acknowledge_s=True)]
        rows = bo.page_rows(views, ROT, NOW)
        self.assertEqual([r['fired'] for r in rows], ['2026-10-17T10:00:00Z', '2026-10-17T10:00:00Z', '2026-10-16T21:30:00Z'])
        self.assertEqual([r['out_of_hours'] for r in rows], [False, False, True])
        self.assertIn(None, [r['acknowledged_by'] for r in rows])  # a name with markup is dropped, not escaped into the data
        self.assertIn(None, [r['time_to_acknowledge_s'] for r in rows])

    def test_weeks_count_and_median(self):
        rows = bo.page_rows([record(), record(time_to_acknowledge_s=60), record(fired='2026-10-08T10:00:00Z')], ROT, NOW)
        w = bo.weeks(rows, NOW)
        self.assertEqual(len(w), bo.WEEKS)
        self.assertEqual(w[-1], {'week': '2026-W42', 'pages': 2, 'out_of_hours': 0, 'median_tta_s': 120})
        self.assertEqual(w[-2]['pages'], 1)
        self.assertEqual(w[0]['pages'], 0)


class ContractTest(unittest.TestCase):
    def setUp(self):
        self.data = bo.build(ROT, [record()], NOW)

    def test_a_good_snapshot_passes_and_renders_the_rows(self):
        bo.check(self.data)
        self.assertIn('Stefan Coetzee', self.data['html'])
        self.assertIn('<code>OllamaDown</code>', self.data['html'])
        self.assertIn('After 15 minutes: responder', self.data['html'])

    def test_breaks_are_refused(self):
        cases = []
        d = copy.deepcopy(self.data); d['pages'][0]['channel'] = 'pager'; cases.append(d)
        d = copy.deepcopy(self.data); d['on_call'][0]['description'] = 'ping 123456789012345678'; cases.append(d)
        d = copy.deepcopy(self.data); d['on_call'][0]['description'] = 'see https://discord.com/x'; cases.append(d)
        d = copy.deepcopy(self.data); d['html'] = d['html'].replace('Stefan', 'Someone'); cases.append(d)
        d = copy.deepcopy(self.data); d['weeks'][0]['pages'] = -1; cases.append(d)
        for d in cases:
            with self.assertRaises(bo.ContractError):
                bo.check(d)

    def test_html_escapes_names(self):
        rot = copy.deepcopy(ROT)
        rot['schedules']['primary']['layers'][0]['name'] = "Waking (o'clock)"
        data = bo.build(rot, [], NOW)
        self.assertIn('Waking (o&#x27;clock)', data['html'])
        self.assertIn('No page has gone through the pager', data['html'])


if __name__ == '__main__':
    result = unittest.main(exit=False).result
    sys.exit(0 if result.wasSuccessful() else 1)
