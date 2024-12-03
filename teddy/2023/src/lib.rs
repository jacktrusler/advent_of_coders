#[macro_export]
macro_rules! read_input {
    () => {{
        std::fs::read_to_string(format!(
            "2023/inputs/{}.txt",
            std::path::PathBuf::from(file!())
                .file_stem()
                .unwrap()
                .to_str()
                .unwrap()
        ))
        .unwrap()
    }};
}
