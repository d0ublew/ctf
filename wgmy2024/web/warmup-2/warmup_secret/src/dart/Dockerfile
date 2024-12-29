FROM dart:3.5 AS build

WORKDIR /app
COPY . .
RUN dart pub get
RUN dart compile exe bin/dart.dart -o bin/dart

FROM scratch

COPY --from=build /runtime/ /
COPY --from=build /app/bin/dart /app/bin/
COPY public/ /app/public/

CMD ["/app/bin/dart"]
