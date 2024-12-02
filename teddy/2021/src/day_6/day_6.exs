defmodule Day6 do
  @moduledoc """
  [Day 6](https://adventofcode.com/2021/day/6): Lanternfish.
  """

  def lanternfish_1(input), do: fishy_count(input, 80)
  def lanternfish_2(input), do: fishy_count(input, 256)
  defp fishy_count(input, 0), do: Map.values(input) |> Enum.sum()

  defp fishy_count(input, iterations) do
    Enum.reduce(input, %{8 => Map.get(input, 0, 0)}, fn
      {0, val}, acc -> Map.update(acc, 6, val, &(&1 + val))
      {key, val}, acc -> Map.update(acc, key - 1, val, &(&1 + val))
    end)
    |> fishy_count(iterations - 1)
  end
end

input =
  File.read!("src/day_6/input.txt")
  |> String.split(~r{\D+}, trim: true)
  |> Stream.map(&String.to_integer/1)
  |> Enum.frequencies()

IO.puts(Day6.lanternfish_1(input))
# 353079
IO.puts(Day6.lanternfish_2(input))
# 1605400130036
