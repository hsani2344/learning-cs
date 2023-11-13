-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Who are these people?
SELECT hour, minute, people.license_plate, name, activity
  FROM bakery_security_logs
  JOIN people
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE hour >= '10'
   AND hour < '11'
   AND day = '28'
   AND month = '7';

-- Let's take a look at transactions
SELECT day, month, name, atm_location, transaction_type, amount
  FROM bank_accounts
  JOIN people
    ON people.id = bank_accounts.person_id
  JOIN atm_transactions
    ON atm_transactions.account_number = bank_accounts.account_number
 WHERE person_id IN
       (SELECT id
          FROM people
          WHERE license_plate IN
                (SELECT license_plate
                   FROM bakery_security_logs
                  WHERE hour > '10'
                    AND day = '28'
                    AND month = '7'))
   AND month >= '7'
   AND transaction_type = 'withdraw'
   AND atm_location = 'Leggett Street'
 ORDER BY month, day;


-- Let's take a look at phone calls
SELECT day, month, caller, receiver, name, duration
  FROM phone_calls
  JOIN people
    ON people.phone_number = phone_calls.caller
 WHERE caller IN
       (SELECT phone_number
          FROM people
         WHERE name = 'Diana'
            OR name = 'Bruce')
    OR receiver IN
       (SELECT phone_number
          FROM people
         WHERE name = 'Diana'
            OR name = 'Bruce');

-- Let's take a look at the interviews
SELECT *
  FROM interviews
 WHERE day >= 28
   AND month >= 7;

-- Flight with bruce or diana from 50ville after the crime
SELECT day, month, hour, minute, name, flight_id, city, abbreviation
  FROM flights
  JOIN airports
    ON airports.id = flights.destination_airport_id
  JOIN passengers
    ON passengers.flight_id = flights.id
  JOIN people
    ON people.passport_number = passengers.passport_number
 WHERE origin_airport_id IN
       (SELECT id FROM airports
         WHERE city = 'Fiftyville')
 ORDER BY month, day, hour, minute, name;
