from pathlib import Path

from mflux import Config, Flux1, ModelLookup, StopImageGenerationException
from mflux.ui.cli.parsers import CommandLineParser


def main():
    # fmt: off
    parser = CommandLineParser(description="Generate an image based on a prompt.")
    parser.add_model_arguments(require_model_arg=False)
    parser.add_lora_arguments()
    parser.add_image_generator_arguments(supports_metadata_config=True)
    parser.add_image_to_image_arguments(required=False)
    parser.add_output_arguments()
    args = parser.parse_args()

    # Load the model
    flux = Flux1(
        model_config=ModelLookup.from_name(model_name=args.model, base_model=args.base_model),
        quantize=args.quantize,
        local_path=args.path,
        lora_paths=args.lora_paths,
        lora_scales=args.lora_scales,
    )

    try:
        for seed_value in args.seed:
            # Generate an image for each seed value
            image = flux.generate_image(
                seed=seed_value,
                prompt=args.prompt,
                stepwise_output_dir=Path(args.stepwise_image_output_dir) if args.stepwise_image_output_dir else None,
                config=Config(
                    num_inference_steps=args.steps,
                    height=args.height,
                    width=args.width,
                    guidance=args.guidance,
                    init_image_path=args.init_image_path,
                    init_image_strength=args.init_image_strength,
                ),
            )
            # Save the image
            image.save(path=args.output.format(seed=seed_value), export_json_metadata=args.metadata)
    except StopImageGenerationException as stop_exc:
        print(stop_exc)


if __name__ == "__main__":
    main()
