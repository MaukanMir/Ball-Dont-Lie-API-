def test_dataframe_operations(df):
    
    assert df.shape == (954, 29)
    assert df.isna().mean().mean() < 0.5