#include <folly/Format.h>

int main()
{
    auto str = folly::format("The answers are {} and {}", 23, 42);
    return EXIT_SUCCESS;
}
