class Solution {
public:
    bool isValid(string s) {
        string prev;
        while (prev != s) {
            prev = s;
            int i = 0;
            while (i < s.length()) {
                if (i + 1 < s.length() &&
                    ((s[i] == '(' && s[i+1] == ')') ||
                     (s[i] == '[' && s[i+1] == ']') ||
                     (s[i] == '{' && s[i+1] == '}'))) {
                    s.erase(i, 2);
                } else {
                    i++;
                }
            }
        }
        return s.empty();
    }
};
