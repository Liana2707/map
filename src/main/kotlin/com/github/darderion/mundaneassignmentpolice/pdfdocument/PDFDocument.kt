package com.github.darderion.mundaneassignmentpolice.pdfdocument

import com.github.darderion.mundaneassignmentpolice.pdfdocument.tables.Table
import com.github.darderion.mundaneassignmentpolice.pdfdocument.text.Line
import mu.KotlinLogging

class PDFDocument(val name: String = "PDF",
				  val text: List<Line>,
				  val tables: List<Table>,
				  val width: Double = defaultPageWidth,
				  val height: Double = defaultPageHeight
				  ) {
	override fun toString() = "PDF: $name\n" +
			text.joinToString("\n") { it.toString() }

	val areas: PDFStructure? = try {
		PDFStructure(text)
	} catch (e: Exception) {
		logger.error(e.message)
		null
	} catch (e: Error) {
		logger.error(e.message)
		null
	}

	fun toHTMLString() = text.joinToString("<br>") { it.content }

	fun getTextFromLines(fromIndex: Int, toIndex: Int, region: PDFRegion) = text.filter { it.area!! inside region }
		.filterIndexed { index, pdfText ->
		index in fromIndex..toIndex
	}.joinToString("\n ") { it.content }

	fun print() {
		text.map { "${it.area} | ${it.text.joinToString("--") { "${it.font.size}-${it.text}"}}" }.forEach(::println)
	}

	private companion object {
		private const val defaultPageHeight = 842.0
		private const val defaultPageWidth = 595.22

		private val logger = KotlinLogging.logger {}
	}
}
