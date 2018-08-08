import pytest
import boto3
import json
import iris_settings
from moto import mock_s3

from iris_data.exceptions import IrisStorageError, IrisDataError
from dlcs_iris_data.tests import expansion_data
from dlcs_iris_data.dlcs_text_iris_data import TextPipelineIrisData


@pytest.fixture()
def moto_boto():

    # start moto
    mock_s3().start()
    resource = boto3.resource('s3')
    client = boto3.client('s3')
    resource.create_bucket(Bucket=iris_settings.IRIS_SESSION_BUCKET)

    # yield
    yield client, resource

    # shutdown mono
    mock_s3().stop()


def test_store_shared_data(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_shared_data(expansion_data.ID1, expansion_data.TEST_JSON_1)

    # check result
    key_name = "shared/" + expansion_data.ID1
    s3 = moto_boto[1]
    bucket = s3.Bucket(iris_settings.IRIS_SESSION_BUCKET)
    keys = list(bucket.objects.filter(Prefix=key_name))
    assert len(keys) == 1
    assert keys[0].key == key_name
    key = s3.Object(iris_settings.IRIS_SESSION_BUCKET, key_name).get()
    key_content = key['Body'].read().decode()
    assert json.dumps(expansion_data.TEST_JSON_1) == key_content


def test_store_retrieve_data(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_shared_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    result = session.get_all_data(expansion_data.ID1)

    assert result == expansion_data.EXPANDED_JSON


def test_get_unexpanded_data(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    result = session.get_unexpanded_data(expansion_data.ID1)

    assert result == expansion_data.EXPANSION_JSON


def test_get_manifest_data(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_shared_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    result = session.get_manifest_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST)

    assert result == expansion_data.MANIFEST_RESULT


def test_get_canvas_data(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_shared_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    result = session.get_canvas_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST, expansion_data.CANVAS_TO_TEST)

    assert result == expansion_data.CANVAS_RESULT


def test_unknown_manifest(moto_boto):

    # run test
    session = TextPipelineIrisData()

    # check result
    with pytest.raises(IrisStorageError):
        session.get_manifest_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST)


def test_unknown_canvas(moto_boto):

    # run test
    session = TextPipelineIrisData()

    # check result
    with pytest.raises(IrisStorageError):
        session.get_canvas_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST, expansion_data.CANVAS_TO_TEST)


def test_unknown_shared(moto_boto):

    # run test
    session = TextPipelineIrisData()

    # don't include required shared data
    # session.store_shared_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    with pytest.raises(IrisStorageError):
        session.get_manifest_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST)


def test_broken_data_manifest(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_data(expansion_data.ID1, expansion_data.BROKEN_EXPANSION_JSON)

    # check result
    with pytest.raises(IrisDataError):
        session.get_manifest_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST)


def test_broken_data_canvas(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_data(expansion_data.ID1, expansion_data.BROKEN_EXPANSION_JSON)

    # check result
    with pytest.raises(IrisDataError):
        session.get_canvas_data(expansion_data.ID1, expansion_data.SERVICE_TO_TEST, expansion_data.CANVAS_TO_TEST)


def test_manifest_data_unknown_service(moto_boto):

    # run test
    session = TextPipelineIrisData()
    session.store_shared_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    session.store_data(expansion_data.ID1, expansion_data.EXPANSION_JSON)

    # check result
    result = session.get_manifest_data(expansion_data.ID1, "UnknownService")

    assert result == {}
