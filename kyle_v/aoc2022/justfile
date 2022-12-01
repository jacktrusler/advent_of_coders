set dotenv-load
session := env_var('AOC_SESSION_KEY')
year := env_var('YEAR')

echo:
  echo 'just works'

day day:
  echo 'day {{day}} works'
  mkdir ./day{{day}}
  cp ./template/* ./day{{day}}
  curl --header "cookie: session={{session}}" https://adventofcode.com/{{year}}/day/{{day}}/input -o ./day{{day}}/input.txt
  cd ./day{{day}} && python -m venv ./venv
  echo 'Done! 🎄🎄 GOOD LUCK! 🎄🎄'
#   make folder and clone template into folder
# download input.txt from aoc
# make virtualenv in day folder

run day:
  cd ./day{{day}} && . ./venv/Scripts/activate && python main.py