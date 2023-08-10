# Test case 1 for Horizon DEX

This App is a tool designed to retrieve and store information about user balances. It interacts with a smart contract to 
obtain balance data and then persists this data in a MongoDB database.

## Table of Contents

- [Endpoints](#endpoints)
  - GET: /balance/current/{wallet_address}
  - GET: /balance/history/{wallet_address}
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Endpoints

### GET: /balance/current/{wallet_address}

This endpoint is used to retrieve the current balance of a user from the associated smart contract. It fetches the 
user's current balance and stores it in the MongoDB database for future reference.

#### Request

- Method: GET
- Path: `/balance/current/{wallet_address}`
- Parameters:
  - `wallet_address`: A valid wallet address of the user whose balance is to be retrieved.

#### Response

```json
{"balance_token": float,"balance_usdt": float}
```

#### DB Object

```json
{
  "_id": mangoDBId,
  "wallet": address str,
  "current_balance": last updated user balance float,
  "current_balance_usd": last updated user balance in USD float,
  "last_update": datetime,
  "history": [
    {
      "date": datetime,
      "token_balance": float,
      "usdt_balance": float
    }, ...
  ]
}
```

### GET: /balance/history/{wallet_address}

This endpoint allows you to fetch the historical balances of a user from the MongoDB database. It provides a record of 
the user's balance changes over time.

#### Request

- Method: GET
- Path: `/balance/history/{wallet_address}`
- Parameters:
  - `wallet_address`: The wallet address of the user whose balance history is to be retrieved.

#### Response

```json
{
  "history": [
    {
      "date": datetime,
      "token_balance": float,
      "usdt_balance": float
    }, ...
  ]
}
```

## Getting Started

To get started with the App, follow these steps:

1. Clone this repository to your local machine.
2. Configure the application (see the [Configuration](#configuration) section).
3. Run the application using the appropriate command (see the [Usage](#usage) section).

## Dependencies

The User Balance App relies on the following dependencies:

- Python 3.9
- Docker
- Docker-compose

## Configuration

Before running the app, you need to set up the configuration using `.env` file.

#### Required env variables:
`DB="<Mango DB connect string>"`

#### Optional env variables:
| Variable           | Default value                                | Comment                                                                        |
|--------------------|----------------------------------------------|--------------------------------------------------------------------------------|
| `WEB3_PROVIDER`    | `https://rpc.eth.gateway.fm`                 | Web3 RPC provider for ETH net                                                  |
| `CONTRACT_ADDRESS` | `0xD533a949740bb3306d119CC777fa900bA034cd52` | Smart contract address                                                         |
| `TOKEN_ID`         | `curve-dao-token`                            | Smart contract token ID for https://www.coingecko.com/ru/api/documentation API |
| `DB_NAME`          | `test_case_1_solovov_db`                     | Mando DB database name                                                         |
|`TABLE_BALANCE`     | `table_balances`                             | Mango DB table name                                                            |

## Usage

To start the application use:
```commandline
sudo docker-compose up
```

## License

The App is open-source software released under the MIT License.

---

Feel free to reach out if you have any questions or need further assistance with the App. Happy coding! 🚀
