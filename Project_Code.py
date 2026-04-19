# ============================================================
#   BRUTE FORCE ATTACK SIMULATION
#   AND SECURE ACCOUNT LOCKOUT MECHANISM
# ============================================================

import time

# ─────────────────────────────────────────
#   USER DATABASE
# ─────────────────────────────────────────
users = {
    "alice": "sunshine99",
    "bob":   "dragon123",
    "carol": "letmein",
}

# ─────────────────────────────────────────
#   ATTACKER'S PASSWORD LIST
# ─────────────────────────────────────────
wordlist = [
    "123456", "password", "hello", "qwerty",
    "abc123", "dragon123", "sunshine99", "letmein",
]

# ─────────────────────────────────────────
#   SECURITY SETTINGS
# ─────────────────────────────────────────
MAX_ATTEMPTS  = 3    # wrong tries before lockout
LOCKOUT_TIME  = 10   # seconds account stays locked
DELAY_PER_FAIL = 1   # extra seconds added per wrong attempt


# ============================================================
#   PART 1 — VULNERABLE LOGIN SYSTEM
#   No protection at all
# ============================================================

def vulnerable_login(username, password):
    if username in users and users[username] == password:
        return True
    return False


# ============================================================
#   PART 2 — SECURE ACCOUNT LOCKOUT MECHANISM
#   Three protections combined
# ============================================================

# These track each user's failed attempts and lockout status
failed_count = {}
locked_until = {}


# Protection 1: Check if account is locked 
def is_locked(username):
    if username in locked_until:
        time_left = locked_until[username] - time.time()
        if time_left > 0:
            print(f"      [LOCKOUT]  Account is LOCKED. "
                  f"{time_left:.0f}s remaining.")
            return True
        else:
            # Lockout expired — reset and unlock
            print(f"      [LOCKOUT]  Lockout expired. Account unlocked.")
            del locked_until[username]
            failed_count[username] = 0
    return False


# Protection 2: Progressive delay
def apply_delay(username):
    count = failed_count.get(username, 0)
    delay = count * DELAY_PER_FAIL
    if delay > 0:
        print(f"      [DELAY]    Waiting {delay}s before processing...")
        time.sleep(delay)


# Protection 3: Count failures and lock if needed 
def record_failure(username):
    failed_count[username] = failed_count.get(username, 0) + 1
    count = failed_count[username]
    print(f"      [COUNTER]  Wrong password. "
          f"Attempt {count}/{MAX_ATTEMPTS}.")

    if count >= MAX_ATTEMPTS:
        locked_until[username] = time.time() + LOCKOUT_TIME
        print(f"      [LOCKOUT]  {MAX_ATTEMPTS} failures reached! "
              f"Account LOCKED for {LOCKOUT_TIME}s.")


# Secured login uses all 3 protections 
def secured_login(username, password):

    # Step 1 — is the account locked?
    if is_locked(username):
        return False

    # Step 2 — apply progressive delay
    apply_delay(username)

    # Step 3 — check the password
    if username in users and users[username] == password:
        failed_count[username] = 0
        print(f"      [LOGIN]    SUCCESS! Welcome {username}.")
        return True
    else:
        record_failure(username)
        return False


# ============================================================
#   PART 3 — BRUTE FORCE ATTACK ENGINE
# ============================================================

def attack(login_function, target):
    print(f"\n   Attacking '{target}' using {len(wordlist)} passwords...\n")
    start = time.time()

    for i, password in enumerate(wordlist, 1):
        print(f"   [{i}] Trying: '{password}'")
        result = login_function(target, password)

        if result:
            elapsed = time.time() - start
            print(f"\n   *** CRACKED! Password = '{password}' "
                  f"| Time = {elapsed:.2f}s ***\n")
            return

    elapsed = time.time() - start
    print(f"\n   >>> Attack STOPPED by security. "
          f"Time = {elapsed:.2f}s <<<\n")


# =============================================
#   PART 4 — LOCKOUT MECHANISM 
# =============================================

def lockout_demo():
    # Reset state for clean demo
    failed_count.clear()
    locked_until.clear()

    print("\n   -- 3 wrong attempts (triggers lockout) --\n")
    secured_login("bob", "wrongpass1")
    print()
    secured_login("bob", "wrongpass2")
    print()
    secured_login("bob", "wrongpass3")

    print("\n   -- Correct password tried while locked --\n")
    secured_login("bob", "dragon123")

    print(f"\n   -- Waiting {LOCKOUT_TIME}s for lockout to expire... --\n")
    time.sleep(LOCKOUT_TIME)

    print("\n   -- Correct password tried after lockout expires --\n")
    secured_login("bob", "dragon123")


# ============================================================
#   DEMO RUN TO SHOW HOW THE ATTACK WORKS AND HOW THE PROTECTIONS STOP IT
# ============================================================

print("=" * 55)
print("   BRUTE FORCE ATTACK SIMULATION")
print("   AND SECURE ACCOUNT LOCKOUT MECHANISM")
print("=" * 55)

# ── Phase 1: Attack vulnerable system ────────────────────────
print("\n>>> PHASE 1: Attacking VULNERABLE system (no protection)")
print("-" * 55)
attack(vulnerable_login, "alice")

# ── Phase 2: Attack secured system ───────────────────────────
print(">>> PHASE 2: Attacking SECURED system (with protection)")
print(f"    max {MAX_ATTEMPTS} attempts | "
      f"{LOCKOUT_TIME}s lockout | "
      f"{DELAY_PER_FAIL}s delay per fail")
print("-" * 55)
attack(secured_login, "alice")

# ── Phase 3: Lockout mechanism step by step ──────────────────
print(">>> PHASE 3: Lockout Mechanism Demo")
print("-" * 55)
lockout_demo()

print("=" * 55)
print("   DEMO COMPLETE")
print("=" * 55)
