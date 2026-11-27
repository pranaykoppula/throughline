#include <bits/stdc++.h>
using namespace std;
#include "solution.cpp"

int main() {
    int n;
    cin >> n;
    vector<vector<int>> courses(n, vector<int>(2));
    for (auto& c : courses) cin >> c[0] >> c[1];
    cout << Solution().scheduleCourse(courses) << "\n";
}
