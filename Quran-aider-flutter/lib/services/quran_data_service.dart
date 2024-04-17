import 'package:flutter/services.dart' show rootBundle;
import 'package:quran_memorization_app/models/chapter.dart';
import 'package:quran_memorization_app/models/verse.dart';
import 'package:xml/xml.dart';
import 'dart:math';

class QuranDataService {
  static Future<List<Chapter>> getChapters() async {
    List<Chapter> chapters = [];
    try {
      // Assuming there are 114 chapters in total
      for (int i = 1; i <= 114; i++) {
        String chapterFileName = i.toString().padLeft(3, '0');
        String chapterDataPath =
            'data/XML/Arabic/Quran_Arabic_$chapterFileName.xml';
        String chapterData = await rootBundle.loadString(chapterDataPath);
        XmlDocument chapterXml = XmlDocument.parse(chapterData);
        XmlElement? chapterElement =
            chapterXml.findAllElements('sura').firstOrNull;

        if (chapterElement != null) {
          String? idAttr = chapterElement.getAttribute('id');
          String? nameAttr = chapterElement.getAttribute('name');
          if (idAttr == null) {
            print('Missing "id" attribute in chapter element: $chapterElement');
            continue; // Skip this element
          }
          int number = int.parse(idAttr);
          String name =
              nameAttr ?? 'Chapter $number'; // Use a default name if missing

          List<Verse> verses = await getVerses(number);
          chapters.add(Chapter(number: number, name: name, verses: verses));
        }
      }
      return chapters;
    } catch (e) {
      print('Error loading chapters: $e');
      throw Exception('Failed to load chapters');
    }
  }

  static Future<List<Verse>> getVerses(int chapterNumber) async {
    try {
      final arabicData = await rootBundle.loadString(
          'data/XML/Arabic/Quran_Arabic_${chapterNumber.toString().padLeft(3, '0')}.xml');
      final englishData = await rootBundle.loadString(
          'data/XML/English/Quran_Translation_Shakir_${chapterNumber.toString().padLeft(3, '0')}.xml');

      final arabicXml = XmlDocument.parse(arabicData);
      final englishXml = XmlDocument.parse(englishData);

      final arabicVerseElements = arabicXml.findAllElements('aya');
      final englishVerseElements = englishXml.findAllElements('aya');

      List<Verse> verses = [];

      final minLength =
          min(arabicVerseElements.length, englishVerseElements.length);
      for (int i = 0; i < minLength; i++) {
        final arabicVerseElement = arabicVerseElements.elementAt(i);
        final englishVerseElement = englishVerseElements.elementAt(i);

        final verseNumber = int.parse(arabicVerseElement.getAttribute('id')!);
        final arabicText = arabicVerseElement.getAttribute('text')!;
        final englishTranslation =
            englishVerseElement.getAttribute('text')!; // Modify this line

        verses.add(Verse(
          verseNumber: verseNumber,
          arabicText: arabicText,
          englishTranslation: englishTranslation,
        ));
      }

      return verses;
    } catch (e) {
      print('Error loading verses for chapter $chapterNumber: $e');
      throw Exception('Failed to load verses for chapter $chapterNumber');
    }
  }
}
