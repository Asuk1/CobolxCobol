       IDENTIFICATION DIVISION.
      * This file contains COBOL test cases for account balance operations.
      * It verifies initial balance and basic logic for the account system.
       PROGRAM-ID. TEST-ACCOUNT.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 TEST-NAME        PIC X(30).
      *-------------------------------------------------------------*
      * Test program for Account System:                            *
      * Verifies initial balance and result logic.                  *
      *-------------------------------------------------------------*
       01 AMOUNT           PIC 9(6)V99.
       01 FINAL-BALANCE    PIC 9(6)V99 VALUE 1000.00.
       01 RESULT           PIC X(10).

      * Declare variables for test name, amount, balance, and result
       PROCEDURE DIVISION.

      * Set up initial test name and balance
           MOVE "Initial Balance" TO TEST-NAME
           MOVE 1000.00 TO FINAL-BALANCE
           IF FINAL-BALANCE = 1000.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Test crediting a valid amount: should increase balance
           MOVE "Credit Valid" TO TEST-NAME
           MOVE 100.00 TO AMOUNT
           ADD AMOUNT TO FINAL-BALANCE
           IF FINAL-BALANCE = 1100.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Test crediting zero amount: should not change balance
           MOVE "Credit Zero" TO TEST-NAME
           MOVE 0.00 TO AMOUNT
           ADD AMOUNT TO FINAL-BALANCE
           IF FINAL-BALANCE = 1100.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Test debiting a valid amount: should decrease balance
           MOVE "Debit Valid" TO TEST-NAME
           MOVE 50.00 TO AMOUNT
           IF FINAL-BALANCE >= AMOUNT
               SUBTRACT AMOUNT FROM FINAL-BALANCE
               IF FINAL-BALANCE = 1050.00
                   MOVE "PASS" TO RESULT
               ELSE
                   MOVE "FAIL" TO RESULT
               END-IF
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Test debit with insufficient funds: should not allow transaction
           MOVE "Debit Insufficient" TO TEST-NAME
           MOVE 2000.00 TO AMOUNT
           IF FINAL-BALANCE >= AMOUNT
               SUBTRACT AMOUNT FROM FINAL-BALANCE
               MOVE "FAIL" TO RESULT
           ELSE
               MOVE "PASS" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Test debiting zero amount: should not change balance
           MOVE "Debit Zero" TO TEST-NAME
           MOVE 0.00 TO AMOUNT
           SUBTRACT AMOUNT FROM FINAL-BALANCE
           IF FINAL-BALANCE = 1050.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

      * Print summary message to indicate completion of all test cases
           DISPLAY "All tests finished."
           STOP RUN.
           
      * End program execution
