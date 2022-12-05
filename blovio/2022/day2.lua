local h = require("2022.lib.helpers")
local file = 'day2.txt'
local lines = h.lines_from(file)

local choice = {
  rock = 1,
  paper = 2,
  scissors = 3,
}
local outcomes = {
  win = 6,
  draw = 3,
  loss = 0,
}

local answers = {}
local p1total = 0;
local p2total = 0;

-- A: Rock | B: Paper | C: Scizzors -- opponent
-- X: Rock | Y: Paper | Z: Scizzors -- you
for _, game in pairs(lines) do
  for opp, my in string.gmatch(game, "(%a) (%a)") do
    local myChoice, result
    if (my == "X") then
      myChoice = choice.rock
      if (opp == "A") then result = outcomes.draw
      elseif opp == "B" then result = outcomes.loss
      else result = outcomes.win
      end
    end
    if my == "Y" then
      myChoice = choice.paper
      if opp == "A" then result = outcomes.win
      elseif opp == "B" then result = outcomes.draw
      else result = outcomes.loss
      end
    end
    if my == "Z" then
      myChoice = choice.scissors
      if opp == "A" then result = outcomes.loss
      elseif opp == "B" then result = outcomes.win
      else result = outcomes.draw
      end
    end
    p1total = result + myChoice + p1total
  end
end
answers.part1 = p1total

for _, game in pairs(lines) do
  for opp, my in string.gmatch(game, "(%a) (%a)") do
    local myChoice, result
    if (my == "X") then
      result = outcomes.loss
      if (opp == "A") then myChoice = choice.scissors
      elseif opp == "B" then myChoice = choice.rock
      else myChoice = choice.paper
      end
    end
    if my == "Y" then
      result = outcomes.draw
      if opp == "A" then myChoice = choice.rock
      elseif opp == "B" then myChoice = choice.paper
      else myChoice = choice.scissors
      end
    end
    if my == "Z" then
      result = outcomes.win
      if opp == "A" then myChoice = choice.paper
      elseif opp == "B" then myChoice = choice.scissors
      else myChoice = choice.rock
      end
    end
    p2total = result + myChoice + p2total
  end
end
answers.part2 = p2total

P(answers)
