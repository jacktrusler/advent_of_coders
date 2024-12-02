defmodule Day2 do
  @moduledoc """
  [Day 2](https://adventofcode.com/2021/day/2): Submarine movement.
  """

  def dive_1(commands) do
    commands
    |> Enum.reduce({0, 0}, fn
      {"forward", dist}, {x, y} -> {x + dist, y}
      {"down", dist}, {x, y} -> {x, y + dist}
      {"up", dist}, {x, y} -> {x, y - dist}
    end)
    |> Tuple.product()
  end

  def dive_2(commands) do
    commands
    |> Enum.reduce({0, 0, 0}, fn
      {"forward", dist}, {aim, x, y} -> {aim, x + dist, y + aim * dist}
      {"down", dist}, {aim, x, y} -> {aim + dist, x, y}
      {"up", dist}, {aim, x, y} -> {aim - dist, x, y}
    end)
    |> then(fn {_, x, y} -> x * y end)
  end
end

input =
  File.stream!("src/day_2/input.txt")
  |> Stream.map(&String.split/1)
  |> Stream.map(fn [dir, dist] -> {dir, String.to_integer(dist)} end)

IO.puts(Day2.dive_1(input))
# 1694130
IO.puts(Day2.dive_2(input))
# 1698850445
