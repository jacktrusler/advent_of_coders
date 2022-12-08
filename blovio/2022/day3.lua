local h = require("lib.helpers")
local file = 'day3.txt'
local lines = h.lines_from(file)
local answers = {}

local function addToSet(set, key)
  set[key] = true
end

local function setContains(set, key)
  return set[key] ~= nil
end

-- Part 1
local answerT1 = {}
for _, v in pairs(lines) do
  local t = {
    fHalf = {},
  }
  for i = 1, #v / 2, 1 do
    addToSet(t.fHalf, string.sub(v, i, i))
  end
  for j = (#v / 2) + 1, #v, 1 do
    local char = string.sub(v, j, j)
    if (setContains(t.fHalf, char)) then
      table.insert(answerT1, char)
      break;
    end
  end
end

answers.part1 = 0;
for _, v in pairs(answerT1) do
  if (string.byte(v) > 90) then
    answers.part1 = answers.part1 + string.byte(v) - 96
  end
  if (string.byte(v) <= 90) then
    answers.part1 = answers.part1 + string.byte(v) - 38
  end
end

-- Part 2
local answerT2 = {}
for i = 1, #lines, 3 do
  local t = {
    l1 = {},
    l2 = {},
    l3 = {},
  }
  for j = 1, #lines[i] do
    addToSet(t.l1, string.sub(lines[i], j, j))
  end
  for k = 1, #lines[i + 1] do
    addToSet(t.l2, string.sub(lines[i + 1], k, k))
  end
  for l = 1, #lines[i + 2] do
    addToSet(t.l3, string.sub(lines[i + 2], l, l))
  end

  for k, _ in pairs(t.l1) do
    if (setContains(t.l2, k)) then
      if (setContains(t.l3, k)) then
        table.insert(answerT2, k)
        break;
      end
    end
  end
end

answers.part2 = 0;
for _, v in pairs(answerT2) do
  if (string.byte(v) > 90) then
    answers.part2 = answers.part2 + string.byte(v) - 96
  end
  if (string.byte(v) <= 90) then
    answers.part2 = answers.part2 + string.byte(v) - 38
  end
end

P(answers)
