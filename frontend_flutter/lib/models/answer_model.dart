class ProcessResponse {
  final bool success;
  final String? question;
  final Map<String, String>? options;
  final List<String> answers;
  final double? confidence;
  final String? message;

  ProcessResponse({
    required this.success,
    this.question,
    this.options,
    required this.answers,
    this.confidence,
    this.message,
  });

  factory ProcessResponse.fromJson(Map<String, dynamic> json) {
    return ProcessResponse(
      success: json['success'],
      question: json['question'],
      options: json['options'] != null
          ? Map<String, String>.from(json['options'])
          : null,
      answers: List<String>.from(json['answers']),
      confidence: json['confidence']?.toDouble(),
      message: json['message'],
    );
  }
}