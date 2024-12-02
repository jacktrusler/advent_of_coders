defmodule Day3 do
  @moduledoc """
  [Day 3](https://adventofcode.com/2021/day/3): Submarine power consumption.
  """

  def power_consumption_1(input) do
    Stream.zip_with(input, & &1)
    |> Stream.map(fn col -> Enum.frequencies(col) |> Enum.max_by(&elem(&1, 1)) |> elem(0) end)
    |> Stream.map(fn
      0 -> {0, 1}
      1 -> {1, 0}
    end)
    |> Enum.unzip()
    |> then(fn {γ, ε} -> Integer.undigits(γ, 2) * Integer.undigits(ε, 2) end)
  end

  def power_consumption_2(input), do: recurse(input, &<=/2) * recurse(input, &>/2)

  defp recurse(input, fun, idx \\ 0) do
    Stream.map(input, &Enum.at(&1, idx))
    |> Enum.frequencies()
    |> then(fn freqs -> (fun.(freqs[0], freqs[1]) && 0) || 1 end)
    |> then(fn min_max -> Enum.filter(input, &(Enum.at(&1, idx) == min_max)) end)
    |> then(fn
      [output] -> Integer.undigits(output, 2)
      output -> recurse(output, fun, idx + 1)
    end)
  end
end

input =
  File.stream!("src/day_3/input.txt")
  |> Stream.map(&String.trim/1)
  |> Stream.map(fn line -> String.graphemes(line) |> Enum.map(&String.to_integer(&1, 2)) end)

IO.puts(Day3.power_consumption_1(input))
# 2250414
IO.puts(Day3.power_consumption_2(input))
# 6085575
