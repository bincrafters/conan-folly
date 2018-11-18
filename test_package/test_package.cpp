#include <cstdlib>
#include <iostream>
#include <utility>
#include <folly/Format.h>
#include <folly/futures/Future.h>
#include <folly/executors/ThreadedExecutor.h>

static void print(const int value) {
    const auto str = folly::format("The answer is {}", value);
    std::cout << str << std::endl;
}

int main() {
    folly::ThreadedExecutor executor;
    folly::Promise<int> promise;
    folly::Future<int> future = promise.getSemiFuture().via(&executor);
    folly::Future<folly::Unit> unit = std::move(future).thenValue(print);
    promise.setValue(42);
    std::move(unit).get();
    return EXIT_SUCCESS;
}
