class ParseTreeVisualizer:
    @staticmethod
    def dump(node, indent=0):
        spacing = "  " * indent
        
        # Jika node bernilai None, kosongkan
        if node is None:
            print(f"{spacing}None")
            return

        # Jika node berupa tipe data primitif (seperti angka int, string, atau boolean)
        if isinstance(node, (int, str, bool)):
            print(f"{spacing}=> {repr(node)}")
            return

        # Jika node berupa objek AST Node kustom kita
        if hasattr(node, '__dict__'):
            print(f"{spacing}[ {node.__class__.__name__} ]")
            for k, v in node.__dict__.items():
                # Jika isinya adalah daftar statement (list)
                if isinstance(v, list):
                    print(f"{spacing}  {k}: [")
                    for item in v:
                        ParseTreeVisualizer.dump(item, indent + 2)
                    print(f"{spacing}  ]")
                else:
                    print(f"{spacing}  {k}:")
                    ParseTreeVisualizer.dump(v, indent + 2)
        else:
            print(f"{spacing}=> {repr(node)}")