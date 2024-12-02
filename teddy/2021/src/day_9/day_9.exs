defmodule Day9 do
  @moduledoc """
  [Day 9](https://adventofcode.com/2021/day/9): Smoke basin.
  """

  @deltas [{99, 0}, {0, 99}, {0, 1}, {1, 0}]

  def heightmap_1(input) do
    lowest(input)
    |> Stream.map(&elem(&1, 0))
    |> Stream.map(&(&1 + 1))
    |> Enum.sum()
  end

  def heightmap_2(input) do
    lowest(input)
    |> Stream.map(fn {n, i} ->
      row = row(i)
      col = col(i, row)

      Stream.map(@deltas, fn {row_delta, col_delta} ->
        {input, (row + row_delta) |> rem(100), (col + col_delta) |> rem(100)}
      end)
    end)
  end

  defp idx(input, row, col), do: Enum.at(input, row * 100 + col)
  defp row(i), do: div(i, 100)
  defp col(i, row), do: i - row * 100

  defp lowest(input) do
    Stream.with_index(input)
    |> Stream.filter(fn {n, i} ->
      row = row(i)
      col = col(i, row)

      Enum.all?(@deltas, fn {row_delta, col_delta} ->
        n < idx(input, (row + row_delta) |> rem(100), (col + col_delta) |> rem(100))
      end)
    end)
  end

  defp recurse_basin(input, n, i) do
    row = row(i)
    col = col(i, row)

    Stream.map(@deltas, fn {row_delta, col_delta} ->
      {input, (row + row_delta) |> rem(100), (col + col_delta) |> rem(100)}
    end)
  end
end

input = File.stream!("src/day_9/input.txt") |> Enum.map(&String.trim/1)
input = Enum.join(input) |> String.graphemes() |> Stream.map(&String.to_integer/1)

# IO.puts(Day9.heightmap_1(input))
# 480
IO.inspect(Day9.heightmap_2(input))
#
