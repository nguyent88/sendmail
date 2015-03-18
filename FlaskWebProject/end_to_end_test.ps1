# End to end test script

$url = "http://localhost:56986/api/sendmail"

# Test cases
$tests = @(
@{
scenario='Well-formed message with one receipt';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","subject":"Test subject","content":"Test content"}';
expected_return_status_code=200;
expected_return_message="sent successfully"
},
@{
scenario='Well-formed message with cc emails';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","cc_email":"trung@outlook.com, trung@gmail.com", "subject":"Test subject","content":"Test content"}';
expected_return_status_code=200;
expected_return_message="sent successfully"
},
@{
scenario='Well-formed message with bcc emails';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","bcc":"trung@outlook, trung@gmail.com", "subject":"Test subject","content":"Test content"}';
expected_return_status_code=200;
expected_return_message="sent successfully"
},
@{
scenario='Well-formed message with cc and bcc emails';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","cc":"trung@gmail.com", "bcc":"trung@outlook.com", "subject":"Test subject","content":"Test content"}';
expected_return_status_code=200;
expected_return_message="sent successfully"
},
@{
scenario='Mal-formed message with no sender';
request='{"to_email":"trung@outlook.com","subject":"Test subject","content":"Test content"}';
expected_return_status_code=400;
expected_return_message="invalid sender email"
},
@{
scenario='Mal-formed message with bad sender email ';
request='{"from_email":"trung@outlook@acb.com","to_email":"trungnd@gmail.com","subject":"Test subject","content":"Test content"}';
expected_return_status_code=400;
expected_return_message="invalid sender email"
},
@{
scenario='Mal-formed message with no receiver';
request='{"from_email":"trung@outlook.com","subject":"Test subject","content":"Test content"}';
expected_return_status_code=400;
expected_return_message="there must be at least one recipient"
},
@{
scenario='Mal-formed message with bad subject';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","subject":"","content":"Test content"}';
expected_return_status_code=400;
expected_return_message="Subject cannot be empty or have more than 1000 characters"
},
@{
scenario='Mal-formed message with bad content';
request='{"from_email":"trung@outlook.com","to_email":"trungnd@gmail.com","subject":"Test","content":""}';
expected_return_status_code=400;
expected_return_message="Content cannot be empty or have more than 10000 characters"
}
)

# Special test case with super long subject
$longSubjectTest = @{
scenario='Mal-formed message with bad, super long subject';
expected_return_status_code=400;
expected_return_message="Subject cannot be empty or have more than 1000 characters"
}
$longSubjectTestRequest = @{from_email='trung@outlook.com';to_email='trungnd@gmail.com';content='Test content'}
$longSubjectTestRequest['subject'] = "Test".PadRight(2000, "A") # create very long subject

$longSubjectTest['request'] = $longSubjectTestRequest 

$tests += $longSubjectTest

# Run all test cases

$totalFailed = 0

foreach ($test in $tests)
{
	"***"
	"Running test scenario: " + $test.scenario
	"Status code:"

	$pass = $true
	try
	{
		$res = Invoke-RestMethod $url -Method Post -Body $test.request -ContentType 'application/json'	
		"Message: Expected: " + $test.expected_return_message + " - Returned: " + $res.message
		"Status code: Expected: " + $test.expected_return_status_code + " - Returned: " + $res.status_code
		if (($res.status_code -ne $test.expected_return_status_code) -or ($res.message.IndexOf($test.expected_return_message,[System.StringComparison]::OrdinalIgnoreCase) -lt 0))
		{		
			$pass = $false
		}
	}
	catch
	{
		"Exception:" + $_.Exception
		$pass = $false
	}

	if (-not $pass)
	{
		$totalFailed++
	}

	"Passed: " + $pass
	"***"
}

"TEST SUMMARY:"
"- Total tests: " + $tests.Count
"- Passed: " + $($tests.Count - $totalFailed)
"- Failed: " + $totalFailed
