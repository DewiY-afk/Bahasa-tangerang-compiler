import sys
import os
from lexer import Lexer
from ast_builder import ASTBuilder
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from codegen import Interpreter
from error_handler import ErrorHandler
from parse_tree import ParseTreeVisualizer

def clear_screen():
    # Fungsi untuk membersihkan terminal agar tampilan selalu bersih
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    filename = "sample.btg"
    
    try:
        with open(filename, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        ErrorHandler.report("System", f"File '{filename}' tidak ditemukan di folder proyek!")
        return

    while True:
        clear_screen()
        print("="*50)
        print("    SISTEM PIPELINE BAHASA TANGERANG COMPILER     ")
        print("="*50)
        print(" [1] Tampilkan Struktur AST / Parse Tree")
        print(" [2] Jalankan Eksekusi Program (.btg)")
        print(" [3] Tampilkan Keduanya (Berurutan)")
        print(" [4] Keluar")
        print("="*50)
        
        pilihan = input("Masukkan pilihan anjeun (1-4): ").strip()
        
        if pilihan == '4':
            print("\nHatur nuhun! Program kaluar.")
            break
            
        if pilihan not in ['1', '2', '3']:
            input("\nPilihan salah! Pencét ENTER jang ngulang...")
            continue
            
        try:
            # Proses kompilasi dasar selalu dijalankan di latar belakang
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            builder = ASTBuilder(tokens)
            ast = builder.build()
            
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            
            optimizer = Optimizer()
            optimized_ast = optimizer.optimize(ast)
            
            clear_screen()
            
            # Kondisi 1: Hanya melihat Pohon Struktur Kode
            if pilihan == '1':
                print("\n" + "="*20 + " STRUKTUR AST / PARSE TREE " + "="*20)
                ParseTreeVisualizer.dump(optimized_ast)
                print("="*67 + "\n")
                
            # Kondisi 2: Hanya menjalankan program Sunda/Tangerang-nya
            elif pilihan == '2':
                print("\n" + "="*20 + " RUNTIME ENGINE OUTPUT " + "="*20)
                interpreter = Interpreter()
                interpreter.execute(optimized_ast)
                print("="*63 + "\n")
                
            # Kondisi 3: Melihat pohon dulu, baru hasil program di bawahnya
            elif pilihan == '3':
                print("\n" + "="*20 + " STRUKTUR AST / PARSE TREE " + "="*20)
                ParseTreeVisualizer.dump(optimized_ast)
                print("="*67)
                
                print("\n" + "="*20 + " RUNTIME ENGINE OUTPUT " + "="*20)
                interpreter = Interpreter()
                interpreter.execute(optimized_ast)
                print("="*63 + "\n")
            
            # Penahan terminal agar output tidak langsung hilang terhapus menu
            input("Pencét ENTER jang balik deui ka menu utama...")
            
        except Exception as e:
            clear_screen()
            ErrorHandler.report("Compiler Pipeline", str(e))
            input("\nPencét ENTER jang balik deui ka menu utama...")

if __name__ == "__main__":
    main()