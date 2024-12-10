# -*- coding: utf-8 -*-
class Memory_DataBase:
    def __init__(self):
        self.mainStorage = {}

        # This is the data to be committed to main storage upon completion of a transaction. 
        self.dataToCommit = {} 
        self.transactionInProgress = False

    def begin_transaction(self):
        if self.transactionInProgress:
            raise Exception("ERROR: A transaction is already active. Only one transaction may occur at a time.")
        self.transactionInProgress = True
        self.dataToCommit = {}

    def put(self, key, value):
        if not self.transactionInProgress:
            raise Exception("ERROR: No active transaction to put.")
        self.dataToCommit[key] = value

    def get(self, key):
        # Only return keys and values that are in main storage.
        return self.mainStorage.get(key, None)

    def commit(self):
        if not self.transactionInProgress:
            raise Exception("ERROR: No active transaction to commit.")

        for k, v in self.dataToCommit.items():
            self.mainStorage[k] = v

        self.transactionInProgress = False
        self.dataToCommit = None

    def rollback(self):
        if not self.transactionInProgress:
            raise Exception("ERROR: No active transition to rollback.")

        self.dataToCommit = None
        self.transactionInProgress = False

# Test cases based off of the expected behavior from the assignment specification.
if __name__ == "__main__":
    inmemoryDB = Memory_DataBase()

    print("Test 1: get('A') before any transaction or data. Expected: None")
    print("Result:", inmemoryDB.get("A"))  # Should return None, because A doesn’t exist

    print("\nTest 2: put('A', 5) without an active transaction. Expected: Exception")
    try:
        inmemoryDB.put("A", 5)
    except Exception as e:
        print("Caught Exception:", e)

    print("\nTest 3: begin_transaction(). Expected: No error, transaction starts")
    inmemoryDB.begin_transaction()

    print("Test 4: put('A', 5) inside an active transaction. Expected: No error")
    inmemoryDB.put("A", 5)

    print("Test 5: get('A') inside transaction but before commit. Expected: None, because changes not committed")
    print("Result:", inmemoryDB.get("A"))

    print("Test 6: put('A', 6) inside the same transaction. Expected: No error")
    inmemoryDB.put("A", 6)

    print("Test 7: commit the transaction. Expected: No error, A=6 committed")
    inmemoryDB.commit()

    print("Test 8: get('A') after commit. Expected: 6")
    print("Result:", inmemoryDB.get("A"))

    print("\nTest 9: commit again without an active transaction. Expected: Exception")
    try:
        inmemoryDB.commit()
    except Exception as e:
        print("Caught Exception:", e)

    print("\nTest 10: rollback without an active transaction. Expected: Exception")
    try:
        inmemoryDB.rollback()
    except Exception as e:
        print("Caught Exception:", e)

    print("\nTest 11: get('B') before transaction and commit. Expected: None")
    print("Result:", inmemoryDB.get("B"))

    print("Test 12: begin_transaction(). Expected: No error, transaction starts")
    inmemoryDB.begin_transaction()

    print("Test 13: put('B', 10) inside an active transaction. Expected: No error")
    inmemoryDB.put("B", 10)

    print("Test 14: rollback transaction. Expected: No error, changes to B discarded")
    inmemoryDB.rollback()

    print("Test 15: get('B') after rollback. Expected: None")
    print("Result:", inmemoryDB.get("B"))
