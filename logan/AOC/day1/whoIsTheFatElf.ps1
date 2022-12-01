$DATA = Get-Content "C:\Users\listl\Desktop\AOC\day1\input.txt"
$currentElf = 0
$elfs = @()
$HaydenElf = 0
$JackElf = 0
$ChrisChistieElf = 0
foreach ($LINE in $DATA)
{
    $currentElf = $currentElf + $LINE
   if ($LINE -lt 0 ){
    $elfs += $currentElf
    $currentElf = 0
   }
}
foreach ($weirdLittleGuy in $elfs){
   if ($weirdLittleGuy -gt $HaydenElf) {
    $HaydenElf = $weirdLittleGuy
   }
   if ($weirdLittleGuy -lt $HaydenElf -and $weirdLittleGuy -gt $JackElf ){
    $JackElf = $weirdLittleGuy
   }
   if ($weirdLittleGuy -lt $JackElf -and $weirdLittleGuy -gt $ChrisChistieElf){
    $ChrisChistieElf = $weirdLittleGuy
   }
}

Write-Output $HaydenElf
Write-Output $JackElf
Write-Output $ChrisChistieElf

$elevatorOverload = $HaydenElf + $JackElf + $ChrisChistieElf

Write-Output $elevatorOverload




