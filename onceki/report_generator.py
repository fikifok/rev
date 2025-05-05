# src/modules/report_generator.py
"""
report_generator.py – PDF ve Excel formatında raporlar üretir.
Kullanım:
    rg = ReportGenerator(output_dir="reports")
    rg.generate_excel_report(df, filename="portfoy_ozet.xlsx", sheet_name="Özet")
    rg.generate_pdf_report(df, filename="portfoy_ozet.pdf", title="Portföy Özeti")
"""

import os
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        """
        Args:
            output_dir (str): Oluşturulacak rapor dosyalarının kaydedileceği klasör.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_excel_report(
        self,
        df: pd.DataFrame,
        filename: str,
        sheet_name: str = "Sheet1"
    ) -> str:
        """
        DataFrame’i Excel dosyası olarak kaydeder.

        Args:
            df (pd.DataFrame): Raporlanacak veri.
            filename (str): Excel dosyası adı (örn. "rapor.xlsx").
            sheet_name (str): Sayfa adı.

        Returns:
            str: Oluşan dosyanın tam yolu.
        """
        path = os.path.join(self.output_dir, filename)
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=True)
        return path

    def generate_pdf_report(
        self,
        df: pd.DataFrame,
        filename: str,
        title: str = "Rapor"
    ) -> str:
        """
        DataFrame’i basit bir tablo halinde PDF’e yazar.

        Args:
            df (pd.DataFrame): Raporlanacak veri.
            filename (str): PDF dosyası adı (örn. "rapor.pdf").
            title (str): PDF başlığı.

        Returns:
            str: Oluşan dosyanın tam yolu.
        """
        path = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = [Paragraph(title, styles['Title']), Spacer(1, 12)]

        # Tablo verisi: önce başlık satırı, sonra her row
        data = [list(df.columns)]
        for row in df.itertuples(index=True):
            data.append(list(row)[1:])  # ilk öğe index, at
        table = Table(data)
        elements.append(table)

        doc.build(elements)
        return path
