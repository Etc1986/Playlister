instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS playlistcontent;',
    'DROP TABLE IF EXISTS playlisttitle;',
    'DROP TABLE IF EXISTS user;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE user(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(150) NOT NULL
        )
    """,
    """
        CREATE TABLE playlisttitle(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description VARCHAR(100) NOT NULL,
            icon  VARCHAR(100) NOT NULL,
            FOREIGN KEY (created_by) REFERENCES user (id)
        )
    """,
    """
        CREATE TABLE playlistcontent(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_for INT NOT NULL,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            year INT,
            genre TEXT NOT NULL,
            FOREIGN KEY (created_for) REFERENCES playlisttitle (id)
        )
    """
]
