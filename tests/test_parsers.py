"""测试 utils/parsers.py 的解析工具函数."""

import pytest

from utils.parsers import (
    format_memory_value,
    parse_float_value,
    parse_integer_value,
    parse_memory_to_kib,
    parse_memory_to_mib,
    parse_memory_value,
)


# ── parse_memory_value ────────────────────────────────────────────────────────

class TestParseMemoryValue:
    def test_gigabytes(self):
        assert parse_memory_value('2G') == 2048          # default target=MiB

    def test_megabytes(self):
        assert parse_memory_value('512M') == 512

    def test_terabytes(self):
        assert parse_memory_value('1T') == 1_048_576

    def test_kilobytes_to_mib(self):
        assert parse_memory_value('1024M') == 1024

    def test_target_kib(self):
        assert parse_memory_value('2G', target_unit='KiB') == 2 * 1024 * 1024

    def test_target_gib(self):
        assert parse_memory_value('2048M', target_unit='GiB') == 2

    def test_no_unit_treated_as_kib(self):
        # 无单位按 KiB 处理，转 MiB 结果为 0（1 KiB < 1 MiB）
        result = parse_memory_value('1024', target_unit='KiB')
        assert result == 1024

    def test_empty_string_returns_default(self):
        assert parse_memory_value('', default=999) == 999

    def test_invalid_string_returns_default(self):
        assert parse_memory_value('invalid', default=42) == 42

    def test_case_insensitive(self):
        assert parse_memory_value('2g') == parse_memory_value('2G')

    def test_gib_suffix(self):
        assert parse_memory_value('1GiB', target_unit='MiB') == 1024

    def test_mib_suffix(self):
        assert parse_memory_value('512MiB') == 512

    def test_kib_suffix(self):
        assert parse_memory_value('1024KiB', target_unit='KiB') == 1024


class TestParseMemoryToKib:
    def test_2g(self):
        assert parse_memory_to_kib('2G') == 2 * 1024 * 1024

    def test_512m(self):
        assert parse_memory_to_kib('512M') == 512 * 1024

    def test_default_on_empty(self):
        assert parse_memory_to_kib('', default=1024) == 1024


class TestParseMemoryToMib:
    def test_2g(self):
        assert parse_memory_to_mib('2G') == 2048

    def test_512m(self):
        assert parse_memory_to_mib('512M') == 512

    def test_default_on_invalid(self):
        assert parse_memory_to_mib('bad', default=1024) == 1024


# ── format_memory_value ───────────────────────────────────────────────────────

class TestFormatMemoryValue:
    def test_mib_to_g(self):
        assert format_memory_value(2048, 'MiB') == '2G'

    def test_kib_to_m(self):
        assert format_memory_value(524_288, 'KiB') == '512M'

    def test_kib_to_g(self):
        assert format_memory_value(2 * 1024 * 1024, 'KiB') == '2G'

    def test_exact_kib(self):
        # 1 KiB — 不能整除 MiB，应返回 K 单位
        assert format_memory_value(1, 'KiB') == '1K'

    def test_mib_to_t(self):
        assert format_memory_value(1024 * 1024, 'MiB') == '1T'


# ── parse_integer_value ───────────────────────────────────────────────────────

class TestParseIntegerValue:
    def test_basic(self):
        assert parse_integer_value('42') == 42

    def test_negative(self):
        assert parse_integer_value('-1') == -1

    def test_invalid_returns_default(self):
        assert parse_integer_value('abc', default=10) == 10

    def test_empty_returns_default(self):
        assert parse_integer_value('', default=5) == 5

    def test_min_clamp(self):
        assert parse_integer_value('0', min_value=1) == 1

    def test_max_clamp(self):
        assert parse_integer_value('100', max_value=50) == 50

    def test_whitespace_stripped(self):
        assert parse_integer_value('  7  ') == 7

    def test_float_string_truncated(self):
        # int('3.14') raises ValueError → default
        assert parse_integer_value('3.14', default=0) == 0


# ── parse_float_value ─────────────────────────────────────────────────────────

class TestParseFloatValue:
    def test_basic(self):
        assert parse_float_value('3.14') == pytest.approx(3.14)

    def test_integer_string(self):
        assert parse_float_value('5') == pytest.approx(5.0)

    def test_invalid_returns_default(self):
        assert parse_float_value('bad', default=1.0) == pytest.approx(1.0)

    def test_empty_returns_default(self):
        assert parse_float_value('', default=2.5) == pytest.approx(2.5)

    def test_min_clamp(self):
        assert parse_float_value('0.0', min_value=0.5) == pytest.approx(0.5)

    def test_max_clamp(self):
        assert parse_float_value('10.0', max_value=5.0) == pytest.approx(5.0)

    def test_negative(self):
        assert parse_float_value('-1.5') == pytest.approx(-1.5)
