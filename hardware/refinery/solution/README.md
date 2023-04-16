# Refinery

Refinery has been a lovely challenge. I think this is my favorite from 2023. It's about PCLs and the modbus protocol. I found various descriptions but I think I used https://www.simplymodbus.ca/FAQ.htm the most.

Let's connect to the service first and try some commands:

```bash
> nc challenges.crysys.hu 5207
> help
Malformed modbus message
> ?
Malformed modbus message
> 01
Invalid device address
...
```

It's talking in modbus language, when I tried sending one byte in hex and got to 42 the error message changed to `Not implemented function` Then I added an other byte to get `Invalid length of message` and finally after adding more and more zeros I get an `Invalid coil address` error.

```
...
> 42
Not implemented function
> 4201
Invalid length of message
> 4202
Not implemented function
> 420100
Invalid length of message
> 42010000
Invalid length of message
> 4201000000
Invalid length of message
> 420100000000
Invalid coil address
>
```

## Understanding the protocol

It's not hard to reverse engineer the protocol using the link from above.

The first number is a `PCL address` it can be 42, 69 or a2. I'm reading this from the png file that was attached to the challenge description.

<img width="565" alt="image" src="https://user-images.githubusercontent.com/6275775/232274544-715233ab-954b-408f-953d-860ff9505013.png">

The next byte is the function, according to the docs it can be one of the following:


| Function Code | Action         | Table Name                      |
|---------------|----------------|---------------------------------|
| 01 (01 hex)   | Read           | Discrete Output Coils           |
| 05 (05 hex)   | Write single   | Discrete Output Coil            |
| 15 (0F hex)   | Write multiple | Discrete Output Coils           |
| 02 (02 hex)   | Read           | Discrete Input Contacts         |
| 04 (04 hex)   | Read           | Analog Input Registers          |
| 03 (03 hex)   | Read           | Analog Output Holding Registers |
| 06 (06 hex)   | Write single   | Analog Output Holding Register  |
| 16 (10 hex)   | Write multiple | Analog Output Holding Registers |

But not everything is supported by the challenge. 

We can read a `coil` with:

`<controller-address>01<coil-address>0001`

the response is:

`<controller-address>01<byte-count><bytes>`

The weirdest part was that coil addresses are off by one compared to what is in the .png. I haven't understand how addressing works, I just tried all possible addresses and wrote down what returned some value. From this I came to the conclusion.

So if we want to read the status of the 'column tank controller'-s 'manual mode' coil we need to write:

`420100690001`

and the result is 

`4201000100`

That is `00` or in other words 'is turned off'. Let's try to turn it on using the `05` function. It has the syntax:

`<controller-address>05<coil-address><value>`

where value can be `ff00` for on and `0000` for off.

`42050069ff00`

Now querying the state: 

`420100690001`

returns:

`4201000180`

I think that's about it. The other type of device is a 'register' that is read with the `04` function code. You need to use it to read the flag and also the e5 and e10 combinator sensors. You can figure out the details on your own.

## Understanding PCL logic:

The third section of the input.png has some ladder diagrams in it:

<img width="755" alt="image" src="https://user-images.githubusercontent.com/6275775/232276449-b588ce36-4e7a-4773-bfaf-46e69e3079aa.png">

I read them as some kind of logic diagrams where `( )` means the trueness of an output device `| |` is true and  `|/|` means false. There are probably better interpretations, but that suffices our purposes.

This means that if we want to turn  `petroleum_input` on we need to `force_start` and `manual_mode` and we should not have the `sensor_high` on. We can control the first two, the last is based on how much petroleum is in the column tank.

Likewise if `sensor_low` is false, `manual_mode` is false then `heater_power` is true.

## Is this thing on?

I created a small Python script that reads the output of all sensors and shows them in a nicely formatted way:

<img width="711" alt="image" src="https://user-images.githubusercontent.com/6275775/232276779-e89434e0-d444-4b95-8e9b-f6d263e680ad.png">

This was really useful to see what's going on.

I added some control logic that turns `manual_mode` on when the sensor is low, and turns it off as soon as we have enough petroleum in the tank (so that the heater can do it's thing).

First I didn't understand what E5 and E10 is, but later I figured that this is the % of ethanol added to the gasoline. So I implemented an other logic that drives the ethanol out coils, and tries to keep the ethanol percentage around 5% and 10% in the corresponding tanks. It's really simple: if the % is too low it turns on the tap, and turns it off when the % is reached.

That's all there is to it. The simulation starts and after about 400 minutes (or 1200 real seconds) the flag register changes. It was around 433 minutes for me.

I should mention that I couldn't capture the flag properly, I might have a bug in my solver, but one of my exception handlers caught it eventually.
