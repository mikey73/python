from model_ds import DataSource


def get_data_sources():
    data_sources = DataSource.objects().distinct('name')
    return data_sources
