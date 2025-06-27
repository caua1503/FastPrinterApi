import argparse
import random
import string


def generate_random_code(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(length))
    return code


def create_env(variables: dict, env_file_path: str = ".env"):
    with open(env_file_path, "w", encoding="utf-8") as f:
        for key, value in variables.items():
            f.write(f"{key}={value}\n")
    print(f"Environment file created at {env_file_path}")


def main():
    variables_default = {
        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "DATABASE_URL": "postgresql+psycopg://postgres:password@127.0.0.1:5432/postgres",
        "DATABASE_LOGS_URL": "postgresql+psycopg://postgres:password@127.0.0.1:5433/postgres",
        "SECRET_KEY": generate_random_code(256),
        "JWT_ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "REDIS_URL": "redis://localhost:6379",
    }

    parser = argparse.ArgumentParser(
        description="Create a .env file with variables",
        epilog="Example: create_env.py -v DB_USER=postgres -v DB_PASSWORD=secret",
    )

    parser.add_argument(
        "-v",
        "--variable",
        action="append",
        help="Variable to add to the .env file",
        metavar="KEY=VALUE",
    )

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=".env",
        help="Path to the output .env file",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help=("list all variables"),
    )

    parser.add_argument(
        "-ld",
        "--list_default",
        action="store_true",
        help=("list all variables with default value"),
    )

    parser.add_argument(
        "-n",
        "--no_interative",
        action="store_true",
        help=("No interative mode"),
    )

    args = parser.parse_args()

    if args.list:
        print("\n")
        for item in variables_default:
            print(item)
        print("\n")

    elif args.list_default:
        print("\n")
        for item, value in variables_default.items():
            print(f"{item} = {value}")
        print("\n")

    elif args.variable:
        for var in args.variable:
            try:
                key, value = var.split("=", 1)
                if key in variables_default:
                    variables_default[key] = value
            except ValueError:
                print(f"Warning: ignoring invalid variable format '{var}'. Format should be KEY=VALUE.")

        create_env(variables_default, args.path)

    elif args.no_interative:
        create_env(variables_default, args.path)

    else:
        question = input("The variable values have not been defined, use default values? (y/N) :")
        if question.lower() != "y":
            print("Exiting...")
            return
        create_env(variables_default, args.path)


if __name__ == "__main__":
    main()
