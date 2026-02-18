import pytest

from seanymph import Figure


# ---------------------------------------------------------------------------
# Categorical x — vertical
# ---------------------------------------------------------------------------

class TestCategoricalVertical:
    x = ["A", "B", "C"]
    y = [1.0, 2.0, 3.0]

    def test_bar(self):
        fig = Figure().bar(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert "xychart-beta\n" in out
        assert "horizontal" not in out
        assert "x-axis [A, B, C]" in out
        assert "bar [1, 2, 3]" in out

    def test_line(self):
        fig = Figure().line(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert "horizontal" not in out
        assert "x-axis [A, B, C]" in out
        assert "line [1, 2, 3]" in out

    def test_bar_and_line(self):
        fig = Figure().bar(self.x, self.y).line(self.x, [4.0, 5.0, 6.0])
        self._figures.append(fig)
        out = fig.render()
        assert "x-axis [A, B, C]" in out
        assert "bar [1, 2, 3]" in out
        assert "line [4, 5, 6]" in out

    def test_multiword_labels_are_quoted(self):
        fig = Figure().bar(["Cat One", "Cat Two"], [1.0, 2.0])
        self._figures.append(fig)
        out = fig.render()
        assert '"Cat One"' in out
        assert '"Cat Two"' in out

    def test_xlabel_appears_before_brackets(self):
        fig = Figure().bar(self.x, self.y).xlabel("Group")
        self._figures.append(fig)
        out = fig.render()
        assert 'x-axis "Group" [A, B, C]' in out

    def test_ylabel_and_ylim(self):
        fig = Figure().bar(self.x, self.y).ylabel("Count").ylim(0, 10)
        self._figures.append(fig)
        out = fig.render()
        assert 'y-axis "Count" 0 --> 10' in out

    def test_ylabel_without_ylim(self):
        fig = Figure().bar(self.x, self.y).ylabel("Count")
        self._figures.append(fig)
        out = fig.render()
        assert 'y-axis "Count"' in out
        assert "-->" not in out

    def test_title(self):
        fig = Figure(title="My Chart").bar(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert 'title "My Chart"' in out

    def test_series_order_preserved(self):
        fig = Figure().bar(self.x, self.y).line(self.x, [4.0, 5.0, 6.0])
        self._figures.append(fig)
        out = fig.render()
        assert out.index("bar") < out.index("line")


# ---------------------------------------------------------------------------
# Categorical x — horizontal
# ---------------------------------------------------------------------------

class TestCategoricalHorizontal:
    x = ["A", "B", "C"]
    y = [1.0, 2.0, 3.0]

    def test_barh(self):
        fig = Figure().barh(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert out.startswith("xychart-beta horizontal")
        assert "x-axis [A, B, C]" in out
        assert "bar [1, 2, 3]" in out

    def test_lineh(self):
        fig = Figure().lineh(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert out.startswith("xychart-beta horizontal")
        assert "x-axis [A, B, C]" in out
        assert "line [1, 2, 3]" in out

    def test_barh_and_lineh(self):
        fig = Figure().barh(self.x, self.y).lineh(self.x, [4.0, 5.0, 6.0])
        self._figures.append(fig)
        out = fig.render()
        assert "xychart-beta horizontal" in out
        assert "bar [1, 2, 3]" in out
        assert "line [4, 5, 6]" in out

    def test_xlabel_with_barh(self):
        fig = Figure().barh(self.x, self.y).xlabel("Group")
        self._figures.append(fig)
        out = fig.render()
        assert 'x-axis "Group" [A, B, C]' in out

    def test_ylabel_with_barh(self):
        fig = Figure().barh(self.x, self.y).ylabel("Value").ylim(0, 5)
        self._figures.append(fig)
        out = fig.render()
        assert 'y-axis "Value" 0 --> 5' in out


# ---------------------------------------------------------------------------
# Numeric x — vertical
# ---------------------------------------------------------------------------

class TestNumericVertical:
    x = [0, 1, 2, 3]
    y = [0.0, 1.0, 4.0, 9.0]

    def test_bar_numeric_range(self):
        fig = Figure().bar(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert "horizontal" not in out
        assert "x-axis 0 --> 3" in out
        assert "bar [0, 1, 4, 9]" in out

    def test_line_numeric_range(self):
        fig = Figure().line(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert "x-axis 0 --> 3" in out
        assert "line [0, 1, 4, 9]" in out

    def test_bar_and_line_numeric(self):
        fig = Figure().bar(self.x, self.y).line(self.x, [1.0, 2.0, 3.0, 4.0])
        self._figures.append(fig)
        out = fig.render()
        assert "x-axis 0 --> 3" in out
        assert "bar [0, 1, 4, 9]" in out
        assert "line [1, 2, 3, 4]" in out

    def test_float_x_values(self):
        fig = Figure().line([0.5, 1.5, 2.5], [10.0, 20.0, 30.0])
        self._figures.append(fig)
        out = fig.render()
        assert "x-axis 0.5 --> 2.5" in out

    def test_xlabel_with_numeric_x(self):
        fig = Figure().line(self.x, self.y).xlabel("Time")
        self._figures.append(fig)
        out = fig.render()
        assert 'x-axis "Time" 0 --> 3' in out

    def test_xlim_overrides_numeric_x_range(self):
        fig = Figure().line(self.x, self.y).xlim(0, 10)
        self._figures.append(fig)
        out = fig.render()
        assert "x-axis 0 --> 10" in out

    def test_ylim_with_numeric_x(self):
        fig = Figure().line(self.x, self.y).ylim(0, 100)
        self._figures.append(fig)
        out = fig.render()
        assert "y-axis 0 --> 100" in out


# ---------------------------------------------------------------------------
# Numeric x — horizontal
# ---------------------------------------------------------------------------

class TestNumericHorizontal:
    x = [10, 20, 30]
    y = [5.0, 15.0, 25.0]

    def test_barh_numeric(self):
        fig = Figure().barh(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert out.startswith("xychart-beta horizontal")
        assert "x-axis 10 --> 30" in out
        assert "bar [5, 15, 25]" in out

    def test_lineh_numeric(self):
        fig = Figure().lineh(self.x, self.y)
        self._figures.append(fig)
        out = fig.render()
        assert out.startswith("xychart-beta horizontal")
        assert "x-axis 10 --> 30" in out
        assert "line [5, 15, 25]" in out

    def test_barh_and_lineh_numeric(self):
        fig = Figure().barh(self.x, self.y).lineh(self.x, [1.0, 2.0, 3.0])
        self._figures.append(fig)
        out = fig.render()
        assert "xychart-beta horizontal" in out
        assert "x-axis 10 --> 30" in out
        assert "bar [5, 15, 25]" in out
        assert "line [1, 2, 3]" in out

    def test_xlabel_with_numeric_horizontal(self):
        fig = Figure().barh(self.x, self.y).xlabel("Index")
        self._figures.append(fig)
        out = fig.render()
        assert 'x-axis "Index" 10 --> 30' in out


# ---------------------------------------------------------------------------
# Number formatting
# ---------------------------------------------------------------------------

class TestNumberFormatting:
    def test_whole_floats_rendered_without_decimal(self):
        fig = Figure().bar(["A"], [2.0])
        self._figures.append(fig)
        out = fig.render()
        assert "bar [2]" in out

    def test_actual_floats_preserved(self):
        fig = Figure().line(["A", "B"], [1.5, 2.7])
        self._figures.append(fig)
        out = fig.render()
        assert "line [1.5, 2.7]" in out

    def test_negative_values(self):
        fig = Figure().bar(["A", "B"], [-5.0, -3.0])
        self._figures.append(fig)
        out = fig.render()
        assert "bar [-5, -3]" in out


# ---------------------------------------------------------------------------
# Validation errors — no figures saved (all tests expect exceptions)
# ---------------------------------------------------------------------------

class TestValidationErrors:
    def test_y_length_mismatch_categorical(self):
        with pytest.raises(ValueError, match="y length"):
            Figure().bar(["A", "B", "C"], [1.0, 2.0])

    def test_y_length_mismatch_numeric(self):
        with pytest.raises(ValueError, match="y length"):
            Figure().bar([1, 2, 3], [1.0, 2.0])

    def test_series_length_mismatch(self):
        with pytest.raises(ValueError, match="y length"):
            Figure().bar(["A", "B"], [1.0, 2.0]).line(["A", "B"], [1.0, 2.0, 3.0])

    def test_x_categories_conflict(self):
        with pytest.raises(ValueError, match="conflict"):
            Figure().bar(["A", "B"], [1.0, 2.0]).line(["X", "Y"], [3.0, 4.0])

    def test_x_numeric_range_conflict(self):
        with pytest.raises(ValueError, match="conflict"):
            Figure().bar([1, 2], [1.0, 2.0]).line([3, 4], [3.0, 4.0])

    def test_mix_vertical_and_horizontal(self):
        with pytest.raises(ValueError, match="Cannot mix"):
            Figure().bar(["A", "B"], [1.0, 2.0]).barh(["A", "B"], [3.0, 4.0])

    def test_mix_line_and_lineh(self):
        with pytest.raises(ValueError, match="Cannot mix"):
            Figure().line(["A", "B"], [1.0, 2.0]).lineh(["A", "B"], [3.0, 4.0])

    def test_non_numeric_y(self):
        with pytest.raises(TypeError, match="not numeric"):
            Figure().bar(["A"], ["oops"])

    def test_infinite_y(self):
        with pytest.raises(ValueError, match="not finite"):
            Figure().bar(["A"], [float("inf")])

    def test_empty_y(self):
        with pytest.raises(ValueError, match="must not be empty"):
            Figure().bar(["A"], [])
