       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST-ACCOUNT.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 TEST-NAME        PIC X(30).
       01 AMOUNT           PIC 9(6)V99.
       01 FINAL-BALANCE    PIC 9(6)V99 VALUE 1000.00.
       01 RESULT           PIC X(10).

       PROCEDURE DIVISION.

           MOVE "Initial Balance" TO TEST-NAME
           MOVE 1000.00 TO FINAL-BALANCE
           IF FINAL-BALANCE = 1000.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

           MOVE "Credit Valid" TO TEST-NAME
           MOVE 100.00 TO AMOUNT
           ADD AMOUNT TO FINAL-BALANCE
           IF FINAL-BALANCE = 1100.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

           MOVE "Credit Zero" TO TEST-NAME
           MOVE 0.00 TO AMOUNT
           ADD AMOUNT TO FINAL-BALANCE
           IF FINAL-BALANCE = 1100.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

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

           MOVE "Debit Insufficient" TO TEST-NAME
           MOVE 2000.00 TO AMOUNT
           IF FINAL-BALANCE >= AMOUNT
               SUBTRACT AMOUNT FROM FINAL-BALANCE
               MOVE "FAIL" TO RESULT
           ELSE
               MOVE "PASS" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

           MOVE "Debit Zero" TO TEST-NAME
           MOVE 0.00 TO AMOUNT
           SUBTRACT AMOUNT FROM FINAL-BALANCE
           IF FINAL-BALANCE = 1050.00
               MOVE "PASS" TO RESULT
           ELSE
               MOVE "FAIL" TO RESULT
           END-IF
           DISPLAY TEST-NAME " : " RESULT

           DISPLAY "All tests finished."
           STOP RUN.
           