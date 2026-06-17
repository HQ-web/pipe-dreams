// pipe_count.cpp
#include <bits/stdc++.h>
using namespace std;


// If you need S_12+, switch this to boost::multiprecision::cpp_int.
// #include <boost/multiprecision/cpp_int.hpp>
// using Count = boost::multiprecision::cpp_int;

using Count = unsigned long long;
using State = uint64_t;

int bits_per_entry(int n) {
    int b = 0;
    int x = n - 1;
    while (x > 0) {
        b++;
        x >>= 1;
    }
    return max(1, b);
}

vector<int> staircase_word(int n) {
    /*
        For S_6:
        5 4 3 2 1
        5 4 3 2
        5 4 3
        5 4
        5

        So Q_6 =
        [5,4,3,2,1, 5,4,3,2, 5,4,3, 5,4, 5]
    */
    vector<int> word;

    for (int row = 1; row <= n - 1; row++) {
        for (int q = n - 1; q >= row; q--) {
            word.push_back(q);
        }
    }

    return word;
}

State pack_perm(const vector<int>& p) {
    int n = (int)p.size();
    int b = bits_per_entry(n);

    if (n * b > 64) {
        throw runtime_error("Permutation too large to pack into uint64_t.");
    }

    State x = 0;

    for (int i = 0; i < n; i++) {
        State value = (State)(p[i] - 1); // store 0-based value
        x |= value << (b * i);
    }

    return x;
}

State pack_identity(int n) {
    int b = bits_per_entry(n);

    if (n * b > 64) {
        throw runtime_error("Permutation too large to pack into uint64_t.");
    }

    State x = 0;

    for (int i = 0; i < n; i++) {
        x |= ((State)i) << (b * i);
    }

    return x;
}

vector<int> unpack_perm(State x, int n) {
    int b = bits_per_entry(n);
    State mask = ((State)1 << b) - 1;

    vector<int> p(n);

    for (int i = 0; i < n; i++) {
        p[i] = (int)((x >> (b * i)) & mask) + 1;
    }

    return p;
}

State right_multiply_simple(State x, int q, int n) {
    /*
        Compute x * s_q.
    */
    int b = bits_per_entry(n);
    State mask = ((State)1 << b) - 1;

    int i = q - 1;

    int shift_a = b * i;
    int shift_b = b * (i + 1);

    State a = (x >> shift_a) & mask;
    State c = (x >> shift_b) & mask;

    State clear_bits = (mask << shift_a) | (mask << shift_b);

    x &= ~clear_bits;

    x |= a << shift_b;
    x |= c << shift_a;

    return x;
}

Count count_pipe_dreams_fast(const vector<int>& target) {
    int n = (int)target.size();

    State identity = pack_identity(n);
    State target_state = pack_perm(target);

    vector<int> Q = staircase_word(n);

    unordered_map<State, Count> dp;
    dp.reserve(1024);
    dp[identity] = 1;

    int b = bits_per_entry(n);

    for (int q : Q) {
        /*
            Snapshot the current layer.

            We mutate dp in-place, but the snapshot prevents states created
            during this step from being processed again during the same step.
        */
        vector<pair<State, Count>> old;
        old.reserve(dp.size());

        for (const auto& kv : dp) {
            old.push_back(kv);
        }

        dp.reserve(dp.size() * 2 + 16);

        for (const auto& [state, count] : old) {
            State next_state = right_multiply_simple(state, q, n);
            dp[next_state] += count;
        }

        cerr << "processed q=" << q
             << ", active states=" << dp.size()
             << "\n";
    }

    auto it = dp.find(target_state);

    if (it == dp.end()) {
        return 0;
    }

    return it->second;
}

int main(int argc, char** argv) {
    /*
        Usage:

            g++ -O3 -std=c++17 pipe_count.cpp -o pipe_count
            ./pipe_count 1 2 3 4 5 6

        That counts pipe dreams for the identity in S_6.

        Another example:

            ./pipe_count 3 1 2 4 5 6
    */

    if (argc < 2) {
        cerr << "Usage: ./pipe_count p1 p2 ... pn\n";
        return 1;
    }

    vector<int> target;

    for (int i = 1; i < argc; i++) {
        target.push_back(stoi(argv[i]));
    }

    int n = (int)target.size();

    vector<int> seen(n + 1, 0);

    for (int x : target) {
        if (x < 1 || x > n || seen[x]) {
            cerr << "Invalid permutation.\n";
            return 1;
        }
        seen[x] = 1;
    }

    Count ans = count_pipe_dreams_fast(target);

    cout << ans << "\n";

    return 0;
}