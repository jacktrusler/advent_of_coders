defmodule Day5 do
  @moduledoc """
  [Day 5](https://adventofcode.com/2021/day/5): Hydrothermal venture.
  """

  defp freq_count(list) do
    Enum.frequencies(list)
    |> Stream.filter(&(elem(&1, 1) >= 2))
    |> Enum.count()
  end

  def hydro_vent_1(input) do
    Stream.filter(input, fn
      [x, _, x, _] -> true
      [_, y, _, y] -> true
      _ -> false
    end)
    |> Stream.flat_map(fn [x1, y1, x2, y2] -> for x <- x1..x2, y <- y1..y2, do: {x, y} end)
    |> freq_count()
  end

  def hydro_vent_2(input) do
    Stream.flat_map(input, fn
      [x, y1, x, y2] -> for y <- y1..y2, do: {x, y}
      [x1, y, x2, y] -> for x <- x1..x2, do: {x, y}
      [x1, y1, x2, y2] -> [x1..x2, y1..y2] |> Stream.map(&Enum.to_list/1) |> Stream.zip()
    end)
    |> freq_count()
  end
end

input =
  File.stream!("src/day_5/input.txt")
  |> Stream.map(&String.trim/1)
  |> Stream.map(&String.split(&1, ~r{\D+}))
  |> Stream.map(fn line -> Enum.map(line, &String.to_integer/1) end)

IO.puts(Day5.hydro_vent_1(input))
# 5084
IO.puts(Day5.hydro_vent_2(input))
# 17882
