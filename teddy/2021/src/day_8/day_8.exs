defmodule Day8 do
  @moduledoc """
  [Day 8](https://adventofcode.com/2021/day/8): Seven segment search.
  """

  def digits_1(input) do
    Stream.map(input, fn {_, outputs} ->
      Stream.map(outputs, &byte_size/1)
      |> Stream.filter(fn size -> size in [2, 3, 4, 7] end)
      |> Enum.count()
    end)
    |> Enum.sum()
  end

  def digits_2(input) do
    Stream.map(input, fn {signals, outputs} ->
      one = Enum.find(signals, &(byte_size(&1) == 2)) |> String.to_charlist()
      four = Enum.find(signals, &(byte_size(&1) == 4)) |> String.to_charlist()
      
      Stream.map(outputs, fn output ->
        case byte_size(output) do
          2 -> 1
          4 -> 4
          3 -> 7
          7 -> 8
          size ->
            case {
              size,
              String.to_charlist(output) |> Stream.filter(&Kernel.in(&1, one)) |> Enum.count(),
              String.to_charlist(output) |> Stream.filter(&Kernel.in(&1, four)) |> Enum.count(),
            } do
              {5, 1, 3} -> 5
              {5, 2, 3} -> 3
              {5, _, 2} -> 2
              {6, 1, _} -> 6
              {6, _, 3} -> 0
              {6, _, 4} -> 9
            end
        end
      end)
      |> Stream.with_index()
      |> Stream.map(fn {output, idx} -> output * 10 ** (3 - idx) end)
      |> Enum.sum()
    end)
    |> Enum.sum()
  end
end

input =
  File.stream!("src/day_8/input.txt")
  |> Stream.map(&String.split(&1, "|"))
  |> Stream.map(fn group -> Enum.map(group, &String.split/1) |> List.to_tuple() end)

IO.puts(Day8.digits_1(input))
# 449
IO.puts(Day8.digits_2(input))
# 968175
