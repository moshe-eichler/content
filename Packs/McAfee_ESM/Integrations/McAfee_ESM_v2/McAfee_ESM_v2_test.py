from freezegun import freeze_time
import pytest
from McAfee_ESM_v2 import *
from McAfee_ESM_v2 import McAfeeESMClient

list_test_filtering_incidents = [
    {'id': 3},
    {'id': 1},
    {'id': 5},
    {'id': 4},
    {'id': 0},
    {'id': 2}
]
data_test_filtering_incidents = [
    (
        (
            0, 0
        ),
        (
            [5, 4, 3, 2, 1]
        )
    ),
    (
        (
            0, 1
        ),
        (
            [1]
        )
    ),
    (
        (
            0, 2
        ),
        (
            [2, 1]
        )
    ),
    (
        (
            3, 1
        ),
        (
            [4]
        )
    ),
    (
        (
            3, 0
        ),
        (
            [5, 4]
        )
    )
]
data_test_expected_errors = [
    ('error', False),
    ('', False),
    ('alarmUnacknowledgeTriggeredAlarm failed with error[ERROR_BadRequest (60)].', True),
    ('alarmAcknowledgeTriggeredAlarm failed with error[ERROR_BadRequest (60)].', True),
    (
        'qryGetResults failed with error[Error deserializing EsmQueryResults, see logs for more information '
        '(Error deserializing EsmQueryResults, see logs for more information '
        '(Internal communication error, see logs for more details))].',
        True
    )
]
data_test_time_format = [
    ('', 'time data \'\' does not match the time format.'),
    ('test', 'time data \'test\' does not match the time format.')
]
data_test_convert_time_format = [
    (('2019-12-19T00:00:00', 0, False), '2019-12-19T00:00:00Z'),
    (('2019-12-19T00:00:00', 2, False), '2019-12-19T02:00:00Z'),
    (('2019-12-19T02:00:00', -2, False), '2019-12-19T00:00:00Z'),
    (('2019-12-19T00:00:00Z', 0, False), '2019-12-19T00:00:00Z'),
    (('2019-12-19T00:00:00Z', 2, False), '2019-12-19T02:00:00Z'),
    (('2019-12-19T02:00:00Z', -2, False), '2019-12-19T00:00:00Z'),
    (('2019/12/19 00:00:00', 0, True), '2019-12-19T00:00:00Z'),
    (('2019/12/19 00:00:00', -2, True), '2019-12-19T02:00:00Z'),
    (('2019/12/19 02:00:00', 2, True), '2019-12-19T00:00:00Z'),

]
data_test_set_query_times = [
    ((None, None, None, 0), ('CUSTOM', None, None)),
    (('1 day', None, None, 0), ('1 day', '2019/12/31 00:00:00', None)),
    (('LAST_WEEK', '', None, 0), ('LAST_WEEK', '', None)),
    (('LAST_YEAR', 'TEST', None, 0), 'Invalid set times.'),
    (('LAST_YEAR', None, 'TEST', 0), 'Invalid set times.'),
    (
        (None, '2020-01-01T00:00:00Z', '2020-01-01T00:00:00Z', 0),
        ('CUSTOM', '2020-01-01T00:00:00Z', '2020-01-01T00:00:00Z')
    )
]
data_test_list_times_set = [
    (
        ([], [], 0),
        []
    ),
    (
        ([0, 0], [], 2),
        [0, 0]
    ),
    (
        (['2019/12/19 00:00:00', '2019/12/19 00:00:00', 0, '2019/12/19 00:00:00'], [0, 1], 0),
        ['2019-12-19T00:00:00Z', '2019-12-19T00:00:00Z', 0, '2019/12/19 00:00:00']
    ),
    (
        ([0, '2019/12/19 00:00:00'], [1], -2),
        [0, '2019-12-19T02:00:00Z']
    ),
    (
        ([0, '2019/12/19 00:00:00'], [], -2),
        [0, '2019/12/19 00:00:00']
    ),
    (
        (['2019/12/19 00:00:00'], [0], -2),
        ['2019-12-19T02:00:00Z']
    )
]
data_test_time_fields = [
    [
        ['time', 'date'],
        [0, 1]
    ],
    [
        ['name', 'TiMe', 'Datetime'],
        [1, 2]
    ],
    [
        [],
        []
    ],
    [
        ['r', 't'],
        []
    ],
    [
        ['', ''],
        []
    ]
]
data_test_mcafee_severity_to_demisto = [(100, 3), (65, 2), (32, 1), (0, 0)]


@pytest.mark.parametrize('test_input, output', data_test_filtering_incidents)
def test_filtering_incidents(test_input, output):
    temp_output = filtering_incidents(list_test_filtering_incidents, test_input[0], test_input[1])
    test_output = [0] * len(temp_output)
    for i in range(len(temp_output)):
        test_output[i] = temp_output[i]['id']
    assert test_output == output, f'filtering_incidents({test_input}) returns: {test_input} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_expected_errors)
def test_expected_errors(test_input, output):
    assert expected_errors(test_input) == output, f'expected_errors({test_input})' \
                                                  f' returns: {not output} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_time_format)
def test_time_format(test_input, output):
    test_output = None
    try:
        test_output = time_format(test_input)
    except ValueError as error:
        test_output = str(error)
    finally:
        assert test_output == output, f'time_format({test_input}) returns error: {test_output} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_convert_time_format)
def test_convert_time_format(test_input, output):
    temp = convert_time_format(test_input[0], test_input[1], test_input[2])
    assert temp == output, f'convert_time_format({test_input[0]}, {test_input[1]}, {test_input[2]}) ' \
                           f'returns: {temp} instead: {output}.'


@freeze_time('2020-01-01 00:00:00')
@pytest.mark.parametrize('test_input, output', data_test_set_query_times)
def test_set_query_times(test_input, output):
    test_output = None
    try:
        test_output = set_query_times(test_input[0], test_input[1], test_input[2], test_input[3])
    except ValueError as error:
        test_output = str(error)
    finally:
        assert test_output == output, f'time_format({test_input}) returns: {test_output} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_list_times_set)
def test_list_times_set(test_input, output):
    temp = list_times_set(test_input[0], test_input[1], test_input[2])
    assert temp == output, f'list_times_set({test_input[0]}, {test_input[1]}, {test_input[2]}) ' \
                           f'returns: {temp} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_time_fields)
def test_time_fields(test_input, output):
    for i in range(len(test_input)):
        test_input[i] = {'name': test_input[i]}
    temp = time_fields(test_input)
    assert temp == output, f'time_fields({test_input}) returns: {temp} instead: {output}.'


@pytest.mark.parametrize('test_input, output', data_test_mcafee_severity_to_demisto)
def test_mcafee_severity_to_demisto(test_input, output):
    temp = mcafee_severity_to_demisto(test_input)
    assert temp == output, f'mcafee_severity_to_demisto({test_input}) returns: {temp} instead: {output}.'


@pytest.mark.filterwarnings('ignore::urllib3.exceptions.InsecureRequestWarning')
def test_edit_case(mocker):
    params = {
        "url": "https://example.com",
        "insecure": True,
        "credentials": {
            "identifier": "TEST",
            "password": "TEST"
        },
        "version": "11.3"}
    raw_response_has_event_list = {"assignedTo": 8207, "closeTime": "2021-05-25T10:29:17Z", "dataSourceList": ["47"],
                                   "deviceList": None,
                                   "eventList": [
                                       {"id": "144117387300438016|6204912068", "lastTime": "2021-05-25T09:47:10Z",
                                        "message": "TEST"}],
                                   "history": "\n------- Viewed: 05/25/2021 10:26:37(GMT)"
                                              "TEST@TEST -------\n\n------- Viewed: 05/25/2021 10:27:34("
                                              "GMT) "
                                              "   TEST@TEST -------\n",
                                   "id": 58136,
                                   "notes": "------- Opened on 2021/05/25 09:53:53(GMT) by Triggered Condition -------"
                                            "\n\n------- In Progress: 05/25/2021 10:29:17(GMT)   Xsoar@TEST -------"
                                            "\n\n------- Changes:  05/25/2021 10:29:17(GMT)   Xsoar@TEST -------"
                                            "\n  Organization\n    old: None\n    new: BRD"
                                            "\n\n", "openTime": "2021-05-25T09:53:53Z",
                                   "orgId": 2, "severity": 50, "statusId": 3,
                                   "summary": "ALERT - Scan"}

    mocker.patch.object(McAfeeESMClient, '_McAfeeESMClient__login', return_value={})
    mocker.patch.object(McAfeeESMClient, '_McAfeeESMClient__request', return_value={})
    mocker.patch.object(McAfeeESMClient, 'get_case_detail', return_value=('', {}, raw_response_has_event_list))
    client = McAfeeESMClient(params)
    client.edit_case()
    result = client._McAfeeESMClient__request.call_args.kwargs['data']['caseDetail']
    assert len(result['eventList']) > 0


class TestTestModule:
    @staticmethod
    def test_sanity(mocker):
        params = {
            "url": "https://example.com",
            "insecure": True,
            "credentials": {
                "identifier": "Shahaf",
                "password": "TEST"
            },
            "version": "11.3"
        }
        mocker.patch.object(McAfeeESMClient, '_McAfeeESMClient__login', return_value={})
        mocker.patch.object(McAfeeESMClient, '_McAfeeESMClient__request', return_value={})
        client = McAfeeESMClient(params)
        _, _, raw = client.test_module()
        assert raw == 'ok'

    @staticmethod
    def test_invalid_starting_id(mocker):
        params = {
            'url': 'https://example.com',
            'insecure': True,
            'credentials': {
                'identifier': 'Shahaf',
                'password': 'TEST',
            },
            'version': '11.3',
            'startingFetchID': '',
            'isFetch': True,
        }
        mocker.patch.object(McAfeeESMClient, '_McAfeeESMClient__login', return_value={})
        mocker.patch.object(McAfeeESMClient, '_http_request')
        mocker.patch.object(demisto, 'params', return_value=params)
        client = McAfeeESMClient(params)
        with pytest.raises(DemistoException):
            client.test_module()
