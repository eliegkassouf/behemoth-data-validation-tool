# behemoth-data-validation-tool
The Behemoth Data Validation Tool (BDVT) is designed to validate and ensure the integrity of extremely large datasets, such as those exceeding 1TB in size. This tool addresses the common challenges faced when dealing with big data validation processes.

**WARNING/ATTENTION**:

Elie Kassouf assumes no responsibility for the use or
reliability of this code.

This code is presented **"as is"** without any guarantees.

**By using this code, you accept any and all risks.**

<hr>

This script is meant to serve as a starting point for your
data validation needs and have not been tested yet. Please
test this script in a development environment before using
it in a production environment. This script is meant to
change with your needs and should be modified to fit your
specific use case.

I used to perform pen testing and the easiest way to brute
force is to use multiple instances because it's faster and
harder to detect. So, I wrote this script to spin up multiple
EC2 instances and assign a specific table to each instance
for validation using the google-data-validation-tool.

If you need more powerful instances, you can change the
instance type to a more powerful one. Be aware that this will
increase the cost of running the instances. Large instances
can be expensive, so be sure to terminate the instances once
the validation is complete to avoid unnecessary charges!

This will ensure that the validation process is faster and
more efficient, especially when dealing with a large number
of tables.

This should be able to handle validation for databases with
1TB or more of data. The google-data-validation-tool is a
powerful tool that can handle large-scale data validation
and provide detailed reports on the validation results.

**Notes**:
1. Make sure to test the scripts in a development environment
   before using them in a production environment.
2. Be sure to terminate the instances once the validation is
   complete to avoid unnecessary charges.
3. The google-data-validation-tool is a powerful tool that can
   handle large-scale data validation and provide detailed
   reports on the validation results.
4. You can use CloudWatch to monitor the instances and set up
   alarms to notify you when the validation is complete. This
   will help you avoid unnecessary charges but will require
   additional configuration from your end.
5. Replace YOUR_SOURCE_CONN, YOUR_TARGET_CONN, YOUR_SCHEMA,
   and YOUR_TARGET_SCHEMA with your actual connection names
   and schema.
6. The columns col1, col2, and col3 are placeholders for your
   actual columns to validate.
7. The UserData script assumes Python3 and pip are available
   in the AMI.