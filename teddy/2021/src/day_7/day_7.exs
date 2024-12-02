defmodule Day7 do
  @moduledoc """
  [Day 7](https://adventofcode.com/2021/day/7): The treachery of whales.
  """

  def crab_1(input) do
    median = Enum.to_list(input) |> int_median()
    input |> Stream.map(&abs(&1 - median)) |> Enum.sum()
  end

  def crab_2(input) do
    mean = Enum.to_list(input) |> int_mean()
    input |> Stream.map(&(1..abs(&1 - mean) |> Enum.sum())) |> Enum.sum()
  end

  defp int_median(input) do
    sorted = Enum.sort(input)
    mid = div(length(input), 2)
    ((Enum.at(sorted, mid - 1) + Enum.at(sorted, mid)) / 2) |> round()
  end

  defp int_mean(input), do: input |> Enum.sum() |> div(length(input))
end

input =
  File.read!("src/day_7/input.txt")
  |> String.split(~r/\D+/, trim: true)
  |> Stream.map(&String.to_integer/1)

IO.puts(Day7.crab_1(input))
# 325528
IO.puts(Day7.crab_2(input))
# 85015836
