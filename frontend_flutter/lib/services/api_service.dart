import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import '../models/answer_model.dart';

class ApiService {
  final String baseUrl;

  // Constructor with optional baseUrl – if provided, overrides the .env value
  ApiService({String? baseUrl}) : baseUrl = baseUrl ?? dotenv.env['API_BASE_URL']!;

  Future<ProcessResponse> processImage(List<int> imageBytes) async {
    final uri = Uri.parse('$baseUrl/api/process-image');

    var request = http.MultipartRequest('POST', uri);
    request.files.add(
      http.MultipartFile.fromBytes(
        'file',
        imageBytes,
        filename: 'image.jpg',
      ),
    );

    final response = await request.send();
    final responseBody = await response.stream.bytesToString();

    if (response.statusCode == 200) {
      final json = jsonDecode(responseBody);
      return ProcessResponse.fromJson(json);
    } else {
      throw Exception('Failed to process image: ${response.statusCode}');
    }
  }
}