from datetime import datetime, timedelta, timezone

from tap_jquants.helpers import convert_json, convert_key, get_next_date


def test_convert_key():
    assert convert_key("CamelCase") == "camel_case"
    assert convert_key("MoreCamelCases") == "more_camel_cases"
    assert convert_key("Sector17CodeName") == "sector17_code_name"
    assert (
        convert_key("CityBKsRegionalBKsEtcSales") == "city_bks_regional_bks_etc_sales"
    )
    # 'Share2nd' is not converted to 'share_2nd'.
    # The only way to do that is to use a dictionary.
    assert (
        convert_key("ResultDividendPerShare2ndQuarter")
        == "result_dividend_per_share2nd_quarter"
    )
    assert convert_key("DistributionsPerUnit(REIT)") == "distributions_per_unit_reit"
    assert convert_key(
        "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock",
    ) == (
        "number_of_issued_and_outstanding_shares_at_the_end_of_fiscal_year"
        "_including_treasury_stock"
    )
    assert convert_key("Volume(OnlyAuction)") == "volume_only_auction"


def test_convert_json():
    assert convert_json(
        {
            "info": [
                {
                    "Date": "2022-11-11",
                    "Code": "86970",
                    "CompanyName": "日本取引所グループ",
                    "CompanyNameEnglish": "Japan Exchange Group,Inc.",
                },
            ],
        },
    ) == {
        "info": [
            {
                "date": "2022-11-11",
                "code": "86970",
                "company_name": "日本取引所グループ",
                "company_name_english": "Japan Exchange Group,Inc.",
            },
        ],
    }


def test_gen_next_date():
    assert get_next_date("2021-01-01") == "2021-01-02"
    assert get_next_date("2021-01-31") == "2021-02-01"
    assert get_next_date("2021-02-28") == "2021-03-01"
    assert get_next_date("2021-12-31") == "2022-01-01"
    assert (
        get_next_date(
            datetime.now(tz=timezone(timedelta(hours=9))).strftime("%Y-%m-%d"),
        )
        is None
    )
