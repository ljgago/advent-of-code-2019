#! /usr/bin/env elixir

# --- Day 8: Space Image Format --- Part Two ---
#
# Now you're ready to decode the image. The image is rendered by stacking the
# layers and aligning the pixels with the same positions in each layer. The
# digits indicate the color of the corresponding pixel: 0 is black, 1 is white,
# and 2 is transparent.
#
# The layers are rendered with the first layer in front and the last layer in
# back. So, if a given position has a transparent pixel in the first and second
# layers, a black pixel in the third layer, and a white pixel in the fourth
# layer, the final image would have a black pixel at that position.
#
# For example, given an image 2 pixels wide and 2 pixels tall, the image data
# 0222112222120000 corresponds to the following image layers:
#
# Layer 1: 02
#          22
#
# Layer 2: 11
#          22
#
# Layer 3: 22
#          12
#
# Layer 4: 00
#          00
#
# Then, the full image can be found by determining the top visible pixel in each
# position:
#
#   - The top-left pixel is black because the top layer is 0.
#   - The top-right pixel is white because the top layer is 2 (transparent), but
#     the second layer is 1.
#   - The bottom-left pixel is white because the top two layers are 2, but the
#     third layer is 1.
#   - The bottom-right pixel is black because the only visible pixel in that
#     position is 0 (from layer 4).
#
# So, the final image looks like this:
#
# 01
# 10
#
# What message is produced after decoding your image?

defmodule PartTwo do
  def image_composer(layers) when is_list(layers) do
    Enum.reduce(layers, hd(layers), fn layer, acc ->
      Enum.zip(acc, layer) |> Enum.map(fn {x, y} ->
        if x === "2", do: y, else: x
      end)
    end)
    |> Enum.map(fn x ->
      if x == "2" or x == "0", do: "\u0020", else: "#"
    end)
    |> List.insert_at(25, "\n")
    |> List.insert_at(51, "\n")
    |> List.insert_at(77, "\n")
    |> List.insert_at(103, "\n")
    |> List.insert_at(129, "\n")
  end
end

# Regex: ~r/.{150}\n?/ - split each 150 = 25*6 characters if it have /n or no
IO.puts("Image:")
File.read!("d8input.txt")
  |> String.split(~r/.{150}\n?/, include_captures: true, trim: true)
  |> Enum.reduce([], fn layer, acc ->
    layer = String.graphemes(layer)
    acc ++ [layer]
  end)
  |> PartTwo.image_composer
  |> IO.puts
