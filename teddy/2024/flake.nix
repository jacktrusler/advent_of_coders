{
  description = "advent-of-code-2023";

  inputs.rust-overlay = {
    url = "github:oxalica/rust-overlay";

    inputs = {
      nixpkgs.follows = "nixpkgs";
      flake-utils.follows = "flake-utils";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      rust-overlay,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs { inherit system overlays; };
        rust = pkgs.rust-bin.fromRustupToolchainFile ./rust-toolchain.toml;
      in
      with pkgs;
      {
        formatter = nixfmt-rfc-style;
        devShells.default = mkShell { packages = [ rust ]; };
      }
    );
}
