import os
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AudioDownloaderApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("新学社 3年リスニング音声ダウンローダー")
    self.geometry("480, 380")
    self.resizable(False, False)

    self.title_label = ctk.CTkLabel(
        self, text="3年リスニング音源 一括ダウンローダー", font=("Helvetica", 16, "bold")
    )
    self.title_label.pack(pady=20)

    self.desc_label = ctk.CTkLabel(
        self,
        text=(
            "レッスン1〜8（合計48ファイル）の音声を\n各レッスン用フォルダに自動で分けて保存します。"
        ),
        justify="center",
    )
    self.desc_label.pack(pady=5)

    self.progress_bar = ctk.CTkProgressBar(self, width=380)
    self.progress_bar.pack(pady=25)
    self.progress_bar.set(0)

    self.status_label = ctk.CTkLabel(
        self, text="準備完了", text_color="gray", font=("Helvetica", 12)
    )
    self.status_label.pack(pady=5)

    self.download_btn = ctk.CTkButton(
        self,
        text="ダウンロード開始",
        command=self.start_download_thread,
        font=("Helvetica", 14, "bold"),
        height=40,
    )
    self.download_btn.pack(pady=20)

  def start_download_thread(self):
    self.download_btn.configure(state="disabled", text="ダウンロード中...")
    threading.Thread(target=self.download_audio_files, daemon=True).start()

  def download_audio_files(self):
    base_output_dir = "downloaded_audio_3nen"
    os.makedirs(base_output_dir, exist_ok=True)

    total_files = 48
    success_count = 0

    try:
      for i in range(1, total_files + 1):
        lesson_num = (i - 1) // 6 + 1
        lesson_dir = os.path.join(base_output_dir, f"lesson{lesson_num}")
        os.makedirs(lesson_dir, exist_ok=True)

        url = f"https://digital2.sing.jp/tyu/jun-lis/audio/HO/ei_junlis_3_sa_{i}.mp3"

        self.status_label.configure(
            text=f"lesson{lesson_num} (ファイル {i}/48) をダウンロード中..."
        )
        self.progress_bar.set(i / total_files)

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
          filepath = os.path.join(lesson_dir, f"ei_junlis_3_sa_{i}.mp3")
          with open(filepath, "wb") as f:
            f.write(response.content)
          success_count += 1

      self.progress_bar.set(1.0)
      self.status_label.configure(text="ダウンロードが完了しました！")
      messagebox.showinfo(
          "完了",
          f"すべてのダウンロードが完了しました！\n\n保存先: 実行フォルダ内の"
          f" `{base_output_dir}`",
      )

    except Exception as e:
      messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")
      self.status_label.configure(text="エラーが発生しました")

    finally:
      self.download_btn.configure(state="normal", text="ダウンロード開始")


if __name__ == "__main__":
  app = AudioDownloaderApp()
  app.mainloop()