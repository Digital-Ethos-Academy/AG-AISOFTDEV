from utils import recommended_models_table

def test_recommended_models_table_provider_filter():
    table = recommended_models_table(provider='openai')
    assert 'gpt-4o' in table
    assert 'claude' not in table

def test_recommended_models_table_task_image():
    table = recommended_models_table(task='image')
    assert 'dall-e-3' in table
    assert 'gpt-4o' not in table
