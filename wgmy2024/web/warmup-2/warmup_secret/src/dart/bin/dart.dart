import 'package:jaguar/jaguar.dart';

void main() async {
  final server = Jaguar(port: 80);
  server.staticFiles('/*', '/app/public');
  server.log.onRecord.listen(print);
  await server.serve(logRequests: true);
}
