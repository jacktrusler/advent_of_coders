defmodule Day4 do
  @moduledoc """
  [Day 4](https://adventofcode.com/2021/day/4): Bingo.
  """

  defp find_win(input, boards) do
    Enum.find(boards, fn {rows, cols} ->
      Enum.any?(rows, &Enum.all?(&1, fn n -> n in input end)) or
        Enum.any?(cols, &Enum.all?(&1, fn n -> n in input end))
    end)
  end

  def bingo_1(input, boards) do
    Enum.reduce_while(input, :none, fn nums, acc ->
      found = find_win(nums, boards)

      if found do
        exclusive_sum =
          Enum.map(elem(found, 0), fn row ->
            Enum.reject(row, fn n -> n in nums end)
            |> Enum.map(&String.to_integer/1)
            |> Enum.sum()
          end)
          |> Enum.sum()

        {:halt, exclusive_sum * (Enum.at(nums, -1) |> String.to_integer())}
      else
        {:cont, acc}
      end
    end)
  end

  def bingo_2(input, boards) do
    winners =
      Enum.reduce(input, [], fn nums, acc ->
        found = find_win(nums, boards)

        if found && elem(found, 0) not in Enum.map(acc, &elem(&1, 1)) do
          [{nums, elem(found, 0)} | acc]
        else
          acc
        end
      end)

    {nums, rows} = Enum.at(winners, 0)

    exclusive_sum =
      Enum.map(rows, fn row ->
        Enum.reject(row, fn n -> n in nums end)
        |> Enum.map(&String.to_integer/1)
        |> Enum.sum()
      end)
      |> Enum.sum()

    exclusive_sum * (Enum.at(nums, -1) |> String.to_integer())
  end
end

[input | boards] =
  File.read!("src/day_4/input.txt")
  |> String.split("\n\n", trim: true)
  |> Enum.map(&String.split(&1, ~r{[\n|,]}, trim: true))

input = Stream.map(1..length(input), &Enum.take(input, &1)) |> Stream.take(-length(input) + 4)

boards =
  Stream.map(boards, fn board -> Enum.map(board, &String.split/1) end)
  |> Enum.map(fn board -> {board, Enum.zip_with(board, & &1)} end)

IO.puts(Day4.bingo_1(input, boards))
# 23177
IO.puts(Day4.bingo_2(input, Enum.reverse(boards)))
# 6804
