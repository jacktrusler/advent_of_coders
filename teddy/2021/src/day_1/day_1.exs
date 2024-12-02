defmodule Day1 do
  @moduledoc """
  [Day 1](https://adventofcode.com/2021/day/1): Sonar sweep thingy.
  """

  def sonar_sweep_1(depths) do
    depths
    |> Stream.chunk_every(2, 1, :discard)
    |> Stream.filter(fn [left, right] -> left < right end)
    |> Enum.count()
  end

  def sonar_sweep_2(depths) do
    depths
    |> Stream.chunk_every(3, 1, :discard)
    |> Stream.map(&Enum.sum/1)
    |> sonar_sweep_1()
  end
end

input =
  File.stream!("src/day_1/input.txt")
  |> Stream.map(&String.trim/1)
  |> Stream.map(&String.to_integer/1)

IO.puts(Day1.sonar_sweep_1(input))
# 1215
IO.puts(Day1.sonar_sweep_2(input))
# 1150
