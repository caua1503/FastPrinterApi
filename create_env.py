import argparse


def create_env(variables: dict, env_file_path: str = ".env"):
    with open(env_file_path, "w") as f:
        for key, value in variables.items():
            f.write(f"{key}={value}\n")
    print(f"Environment file created at {env_file_path}")


def main():
    variables = {}

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

    args = parser.parse_args()

    if args.variable:
        for var in args.variable:
            try:
                key, value = var.split("=", 1)
                variables[key] = value
            except ValueError:
                print(f"Warning: ignoring invalid variable format '{var}'. Format should be KEY=VALUE.")
    else:
        question = input("the variable values have not been defined, use default values? (y/n)")
        if question.lower() != "y":
            print("Exiting...")
            return
        variables = {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "REDIS_DB": "0",
            "REDIS_PASSWORD": "password",
            "DATABASE_URL": "postgresql+psycopg://postgres:password@localhost:5432/postgres",
            "SECRET_KEY": "secret",
            "JWT_ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        }

    create_env(variables, args.path)


if __name__ == "__main__":
    main()
